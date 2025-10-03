"""Memory management utilities for LangChain LLM."""
from typing import List, Dict, Any, Optional
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from datetime import datetime
import os

from config import Config


class LongTermMemory:
    """Long-term memory implementation using ChromaDB vector store."""
    
    def __init__(self, persist_directory: str = None, collection_name: str = None):
        """Initialize long-term memory with vector store.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
            collection_name: Name of the collection in ChromaDB
        """
        self.persist_directory = persist_directory or Config.CHROMA_DB_DIR
        self.collection_name = collection_name or Config.COLLECTION_NAME
        
        # Create directory if it doesn't exist
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=Config.EMBEDDING_MODEL,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        # Initialize or load vector store
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
    
    def add_conversation(self, user_message: str, ai_message: str, metadata: Dict[str, Any] = None):
        """Add a conversation exchange to long-term memory.
        
        Args:
            user_message: User's message
            ai_message: AI's response
            metadata: Additional metadata for the conversation
        """
        timestamp = datetime.now().isoformat()
        
        # Prepare metadata
        doc_metadata = {
            "timestamp": timestamp,
            "type": "conversation",
            **(metadata or {})
        }
        
        # Create document with conversation context
        conversation_text = f"User: {user_message}\nAssistant: {ai_message}"
        document = Document(
            page_content=conversation_text,
            metadata=doc_metadata
        )
        
        # Add to vector store
        self.vectorstore.add_documents([document])
    
    def retrieve_relevant_memories(self, query: str, k: int = None) -> List[Document]:
        """Retrieve relevant memories based on query.
        
        Args:
            query: Query string to search for
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        k = k or Config.RETRIEVAL_K
        results = self.vectorstore.similarity_search(query, k=k)
        return results
    
    def get_context_from_memories(self, query: str, k: int = None) -> str:
        """Get formatted context string from relevant memories.
        
        Args:
            query: Query string to search for
            k: Number of results to return
            
        Returns:
            Formatted context string
        """
        memories = self.retrieve_relevant_memories(query, k)
        
        if not memories:
            return ""
        
        context_parts = ["Relevant past conversations:"]
        for i, doc in enumerate(memories, 1):
            context_parts.append(f"\n{i}. {doc.page_content}")
        
        return "\n".join(context_parts)
    
    def clear_memory(self):
        """Clear all memories from the vector store."""
        # Delete the collection and recreate
        self.vectorstore.delete_collection()
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )


class ShortTermMemory:
    """Short-term memory implementation using conversation buffer."""
    
    def __init__(self, window_size: int = None):
        """Initialize short-term memory with conversation buffer.
        
        Args:
            window_size: Number of recent messages to keep in buffer
        """
        self.window_size = window_size or Config.CONVERSATION_BUFFER_SIZE
        self.memory = ConversationBufferWindowMemory(
            k=self.window_size,
            memory_key=Config.MEMORY_KEY,
            return_messages=True
        )
    
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]):
        """Save conversation context to memory.
        
        Args:
            inputs: Input dictionary with user message
            outputs: Output dictionary with AI response
        """
        self.memory.save_context(inputs, outputs)
    
    def load_memory_variables(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Load memory variables.
        
        Args:
            inputs: Optional inputs dictionary
            
        Returns:
            Memory variables dictionary
        """
        return self.memory.load_memory_variables(inputs or {})
    
    def clear(self):
        """Clear the conversation buffer."""
        self.memory.clear()
    
    def get_buffer(self) -> List[Any]:
        """Get the current conversation buffer.
        
        Returns:
            List of messages in the buffer
        """
        return self.memory.chat_memory.messages


class HybridMemory:
    """Hybrid memory combining short-term and long-term memory."""
    
    def __init__(self, short_term: ShortTermMemory = None, long_term: LongTermMemory = None):
        """Initialize hybrid memory system.
        
        Args:
            short_term: Short-term memory instance
            long_term: Long-term memory instance
        """
        self.short_term = short_term or ShortTermMemory()
        self.long_term = long_term or LongTermMemory()
    
    def add_exchange(self, user_message: str, ai_message: str, metadata: Dict[str, Any] = None):
        """Add conversation exchange to both memory systems.
        
        Args:
            user_message: User's message
            ai_message: AI's response
            metadata: Additional metadata
        """
        # Save to short-term memory
        self.short_term.save_context(
            {"input": user_message},
            {"output": ai_message}
        )
        
        # Save to long-term memory
        self.long_term.add_conversation(user_message, ai_message, metadata)
    
    def get_full_context(self, current_query: str) -> Dict[str, Any]:
        """Get full context from both memory systems.
        
        Args:
            current_query: Current user query
            
        Returns:
            Dictionary with short-term and long-term context
        """
        # Get short-term context
        short_term_context = self.short_term.load_memory_variables({})
        
        # Get long-term context
        long_term_context = self.long_term.get_context_from_memories(current_query)
        
        return {
            "short_term": short_term_context,
            "long_term": long_term_context
        }
    
    def clear_all(self):
        """Clear both memory systems."""
        self.short_term.clear()
        self.long_term.clear_memory()
