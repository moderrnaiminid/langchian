"""Professional LangChain LLM with comprehensive long-term memory."""
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from config import Config
from memory_manager import HybridMemory, LongTermMemory, ShortTermMemory


class ProfessionalLLM:
    """Professional LLM with hybrid memory system for intelligent conversations."""
    
    SYSTEM_PROMPT_TEMPLATE = """You are a highly professional and intelligent AI assistant with access to long-term memory. 
You can remember past conversations and use that context to provide more personalized and relevant responses.

{long_term_context}

Current conversation context:
{chat_history}

Instructions:
- Be professional, helpful, and accurate in your responses
- Use information from past conversations when relevant
- Acknowledge when you remember something from a previous conversation
- If you don't have relevant past context, focus on the current query
- Maintain consistency with information shared in past conversations
"""
    
    def __init__(
        self, 
        model_name: str = None,
        temperature: float = None,
        max_tokens: int = None,
        use_long_term_memory: bool = True
    ):
        """Initialize the Professional LLM.
        
        Args:
            model_name: Name of the OpenAI model to use
            temperature: Temperature parameter for generation
            max_tokens: Maximum tokens in response
            use_long_term_memory: Whether to use long-term memory
        """
        # Validate configuration
        Config.validate()
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model_name or Config.MODEL_NAME,
            temperature=temperature or Config.TEMPERATURE,
            max_tokens=max_tokens or Config.MAX_TOKENS,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        # Initialize memory systems
        self.use_long_term_memory = use_long_term_memory
        if use_long_term_memory:
            self.memory = HybridMemory()
        else:
            self.memory = ShortTermMemory()
    
    def chat(self, message: str, metadata: Dict[str, Any] = None) -> str:
        """Send a message to the LLM and get a response.
        
        Args:
            message: User message
            metadata: Optional metadata for the conversation
            
        Returns:
            AI response
        """
        # Get context from memory
        if self.use_long_term_memory:
            context = self.memory.get_full_context(message)
            long_term_context = context.get("long_term", "")
            short_term_messages = context.get("short_term", {}).get(Config.MEMORY_KEY, [])
        else:
            long_term_context = ""
            short_term_messages = self.memory.load_memory_variables({}).get(Config.MEMORY_KEY, [])
        
        # Build messages for the LLM
        messages = []
        
        # Add system message with context
        system_content = self.SYSTEM_PROMPT_TEMPLATE.format(
            long_term_context=long_term_context if long_term_context else "No relevant past conversations found.",
            chat_history="" if not short_term_messages else "Recent conversation history available."
        )
        messages.append(SystemMessage(content=system_content))
        
        # Add short-term conversation history
        if short_term_messages:
            messages.extend(short_term_messages)
        
        # Add current user message
        messages.append(HumanMessage(content=message))
        
        # Get response from LLM
        response = self.llm.invoke(messages)
        ai_message = response.content
        
        # Save to memory
        if self.use_long_term_memory:
            self.memory.add_exchange(message, ai_message, metadata)
        else:
            self.memory.save_context(
                {"input": message},
                {"output": ai_message}
            )
        
        return ai_message
    
    def clear_memory(self, clear_long_term: bool = False):
        """Clear memory.
        
        Args:
            clear_long_term: Whether to clear long-term memory as well
        """
        if self.use_long_term_memory:
            self.memory.short_term.clear()
            if clear_long_term:
                self.memory.long_term.clear_memory()
        else:
            self.memory.clear()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about memory usage.
        
        Returns:
            Dictionary with memory statistics
        """
        stats = {}
        
        if self.use_long_term_memory:
            stats["short_term_messages"] = len(self.memory.short_term.get_buffer())
            stats["short_term_window_size"] = self.memory.short_term.window_size
        else:
            stats["short_term_messages"] = len(self.memory.get_buffer())
            stats["short_term_window_size"] = self.memory.window_size
        
        return stats


def create_llm(
    model_name: str = None,
    temperature: float = None,
    max_tokens: int = None,
    use_long_term_memory: bool = True
) -> ProfessionalLLM:
    """Factory function to create a Professional LLM instance.
    
    Args:
        model_name: Name of the OpenAI model to use
        temperature: Temperature parameter for generation
        max_tokens: Maximum tokens in response
        use_long_term_memory: Whether to use long-term memory
        
    Returns:
        Configured ProfessionalLLM instance
    """
    return ProfessionalLLM(
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        use_long_term_memory=use_long_term_memory
    )
