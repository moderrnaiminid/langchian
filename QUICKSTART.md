# Quick Start Guide

This guide will help you get up and running with the LangChain Professional LLM in 5 minutes.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- LangChain and related packages
- OpenAI API client
- ChromaDB (vector database)
- Python-dotenv (environment management)

## Step 2: Set Up Your API Key

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

You can get an API key from: https://platform.openai.com/api-keys

## Step 3: Run Your First Example

### Option A: Run the Example Script

```bash
python example.py
```

This will run through several demonstrations and then offer an interactive mode.

### Option B: Quick Python Script

Create a file `test.py`:

```python
from llm_app import create_llm

# Create the LLM
llm = create_llm()

# Have a conversation
print(llm.chat("Hello! My name is Alice."))
print(llm.chat("What's my name?"))
```

Run it:
```bash
python test.py
```

## Step 4: Interactive Mode

For interactive testing:

```bash
python example.py
```

Then choose 'y' when prompted for interactive mode.

Commands:
- Just type to chat
- `exit` - Quit
- `clear` - Clear short-term memory
- `stats` - Show memory statistics

## Understanding Memory

### Short-Term Memory
- Keeps the last 10 messages in conversation buffer
- Fast access, immediate context

### Long-Term Memory
- Stores all conversations in vector database
- Retrieves relevant past conversations based on similarity
- Persists across sessions

### Example:

```python
from llm_app import create_llm

llm = create_llm()

# First conversation
llm.chat("I love Python programming.")
llm.chat("My favorite framework is Django.")

# Later (even in a new session)
llm2 = create_llm()
response = llm2.chat("What do you know about my preferences?")
# Will remember Python and Django!
```

## Configuration Options

Edit `.env` to customize:

```env
# Use GPT-4 for better responses (more expensive)
MODEL_NAME=gpt-4

# Lower temperature for more focused responses
TEMPERATURE=0.5

# Increase conversation buffer
CONVERSATION_BUFFER_SIZE=20

# Retrieve more past memories
RETRIEVAL_K=10
```

## Troubleshooting

### "OPENAI_API_KEY is not set"
Make sure you:
1. Created the `.env` file
2. Added your API key
3. The key starts with `sk-`

### "No module named 'langchain'"
Install dependencies:
```bash
pip install -r requirements.txt
```

### Slow responses
Reduce the number of retrieved memories:
```env
RETRIEVAL_K=3
```

### Memory not working
Delete the database and restart:
```bash
rm -rf chroma_db/
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore `example.py` for more usage patterns
3. Check out the code in `llm_app.py` and `memory_manager.py`
4. Customize the system prompt in `llm_app.py`

## Cost Considerations

- GPT-3.5-turbo: ~$0.002 per 1K tokens
- GPT-4: ~$0.03 per 1K tokens
- Embeddings: ~$0.0001 per 1K tokens

Start with `gpt-3.5-turbo` for testing!

## Getting Help

- Check the [README.md](README.md) for full documentation
- Review the code examples in `example.py`
- Open an issue on GitHub for bugs or questions

Happy coding! 🚀
