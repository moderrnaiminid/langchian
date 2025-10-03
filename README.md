# LangChain Professional LLM with Long-Term Memory

A professional, production-ready implementation of a LangChain-based Large Language Model (LLM) with comprehensive long-term memory capabilities. This project combines short-term conversation buffers with vector-based long-term memory storage to create an intelligent AI assistant that remembers past conversations and provides contextually aware responses.

## Features

### 🧠 Hybrid Memory System
- **Short-Term Memory**: Conversation buffer that maintains recent conversation context
- **Long-Term Memory**: Vector store-based persistent memory using ChromaDB
- **Intelligent Retrieval**: Automatically retrieves relevant past conversations based on semantic similarity

### 🚀 Professional Architecture
- **Modular Design**: Separate components for memory management, configuration, and LLM operations
- **Configurable**: Easy configuration via environment variables or `.env` file
- **Scalable**: Built with production use in mind

### 💡 Key Capabilities
- Remembers user preferences and information across sessions
- Contextual responses based on conversation history
- Metadata support for categorizing conversations
- Memory statistics and management
- Interactive chat mode

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/moderrnaiminid/langchian.git
cd langchian
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Configuration

All configuration is managed through environment variables. You can set these in a `.env` file:

```env
# OpenAI API Key (Required)
OPENAI_API_KEY=your_openai_api_key_here

# LLM Model Settings
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=2000

# Memory Settings
CONVERSATION_BUFFER_SIZE=10

# Vector Store Settings
CHROMA_DB_DIR=./chroma_db
COLLECTION_NAME=long_term_memory
EMBEDDING_MODEL=text-embedding-ada-002

# Retrieval Settings
RETRIEVAL_K=5
```

### Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `MODEL_NAME` | OpenAI model to use | `gpt-3.5-turbo` |
| `TEMPERATURE` | Response randomness (0-1) | `0.7` |
| `MAX_TOKENS` | Maximum response length | `2000` |
| `CONVERSATION_BUFFER_SIZE` | Short-term memory window | `10` |
| `CHROMA_DB_DIR` | Directory for vector store | `./chroma_db` |
| `COLLECTION_NAME` | ChromaDB collection name | `long_term_memory` |
| `EMBEDDING_MODEL` | Model for embeddings | `text-embedding-ada-002` |
| `RETRIEVAL_K` | Number of memories to retrieve | `5` |

## Usage

### Quick Start

```python
from llm_app import create_llm

# Create LLM instance with long-term memory
llm = create_llm(use_long_term_memory=True)

# Have a conversation
response = llm.chat("Hello! My name is Alice and I love Python.")
print(response)

# The LLM will remember this in future conversations
response = llm.chat("What's my name?")
print(response)  # Will remember "Alice"
```

### Running Examples

The project includes comprehensive examples:

```bash
python example.py
```

This will run through several examples demonstrating:
1. Basic conversation with memory
2. Memory persistence across sessions
3. Using metadata with conversations
4. Memory management (clearing)
5. Interactive chat mode

### Interactive Mode

For interactive testing:

```bash
python example.py
# Follow prompts to enter interactive mode
```

Commands in interactive mode:
- Type your message to chat
- `exit` - Quit the application
- `clear` - Clear short-term memory
- `stats` - Show memory statistics

## Architecture

### Components

#### 1. `llm_app.py` - Main LLM Application
The core LLM implementation with hybrid memory integration.

```python
from llm_app import ProfessionalLLM

llm = ProfessionalLLM(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    use_long_term_memory=True
)
```

#### 2. `memory_manager.py` - Memory Management
Handles both short-term and long-term memory:

- **ShortTermMemory**: Conversation buffer for recent context
- **LongTermMemory**: Vector store for persistent memory
- **HybridMemory**: Combines both memory types

```python
from memory_manager import HybridMemory

memory = HybridMemory()
memory.add_exchange("User message", "AI response")
context = memory.get_full_context("Current query")
```

#### 3. `config.py` - Configuration Management
Centralized configuration with validation.

```python
from config import Config

Config.validate()  # Validates required settings
model = Config.MODEL_NAME
```

### Memory Flow

1. **User sends message** → System retrieves relevant long-term memories
2. **LLM receives**:
   - Current message
   - Short-term conversation buffer
   - Relevant long-term memories
3. **LLM generates response** → Saved to both memory systems
4. **Future queries** → Can access all past context

## Advanced Usage

### Custom Configuration

```python
from llm_app import create_llm

# Create with custom settings
llm = create_llm(
    model_name="gpt-4",
    temperature=0.5,
    max_tokens=3000,
    use_long_term_memory=True
)
```

### Adding Metadata

```python
# Add conversation with metadata
response = llm.chat(
    "Remember: Project deadline is December 15th",
    metadata={
        "type": "important",
        "category": "deadline",
        "priority": "high"
    }
)
```

### Memory Management

```python
# Get memory statistics
stats = llm.get_memory_stats()
print(f"Short-term messages: {stats['short_term_messages']}")

# Clear short-term memory only
llm.clear_memory(clear_long_term=False)

# Clear all memory
llm.clear_memory(clear_long_term=True)
```

### Accessing Memory Components Directly

```python
# Access hybrid memory
hybrid_memory = llm.memory

# Get specific memories
if hasattr(hybrid_memory, 'long_term'):
    memories = hybrid_memory.long_term.retrieve_relevant_memories(
        query="What did we discuss about Python?",
        k=3
    )
```

## Project Structure

```
langchian/
├── .env.example          # Example environment configuration
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── requirements.txt     # Python dependencies
├── config.py           # Configuration management
├── memory_manager.py   # Memory system implementation
├── llm_app.py         # Main LLM application
├── example.py         # Usage examples
└── chroma_db/         # Vector store data (auto-created)
```

## Best Practices

1. **API Key Security**: Never commit your `.env` file with real API keys
2. **Memory Management**: Periodically clear old long-term memories if needed
3. **Cost Optimization**: Use `gpt-3.5-turbo` for cost-effective operations
4. **Error Handling**: Wrap LLM calls in try-except blocks for production
5. **Monitoring**: Track memory stats to understand usage patterns

## Troubleshooting

### Common Issues

**Issue**: "OPENAI_API_KEY is not set"
- **Solution**: Ensure `.env` file exists with valid API key

**Issue**: ChromaDB errors
- **Solution**: Delete `chroma_db/` directory and restart

**Issue**: Memory not persisting
- **Solution**: Ensure `use_long_term_memory=True` when creating LLM

**Issue**: Slow responses
- **Solution**: Reduce `RETRIEVAL_K` in configuration

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain) - Framework for LLM applications
- [OpenAI](https://openai.com/) - LLM and embedding models
- [ChromaDB](https://www.trychroma.com/) - Vector database for long-term memory

## Support

For questions or issues, please open an issue on GitHub.
