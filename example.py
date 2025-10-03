"""Example usage of the Professional LangChain LLM with long-term memory."""
import os
from llm_app import create_llm


def example_basic_conversation():
    """Example of basic conversation with the LLM."""
    print("=" * 60)
    print("Example 1: Basic Conversation")
    print("=" * 60)
    
    # Create LLM instance with long-term memory
    llm = create_llm(use_long_term_memory=True)
    
    # Have a conversation
    print("\n>>> User: Hello! My name is Alice and I'm a software engineer.")
    response = llm.chat("Hello! My name is Alice and I'm a software engineer.")
    print(f">>> Assistant: {response}")
    
    print("\n>>> User: What are the best practices for Python development?")
    response = llm.chat("What are the best practices for Python development?")
    print(f">>> Assistant: {response}")
    
    print("\n>>> User: What's my name again?")
    response = llm.chat("What's my name again?")
    print(f">>> Assistant: {response}")
    
    # Show memory stats
    stats = llm.get_memory_stats()
    print(f"\n>>> Memory Stats: {stats}")


def example_memory_persistence():
    """Example showing long-term memory persistence across sessions."""
    print("\n" + "=" * 60)
    print("Example 2: Memory Persistence Across Sessions")
    print("=" * 60)
    
    # First session
    print("\n--- Session 1 ---")
    llm1 = create_llm()
    
    print("\n>>> User: I love Python programming and machine learning.")
    response = llm1.chat("I love Python programming and machine learning.")
    print(f">>> Assistant: {response}")
    
    print("\n>>> User: My favorite framework is TensorFlow.")
    response = llm1.chat("My favorite framework is TensorFlow.")
    print(f">>> Assistant: {response}")
    
    # Simulate new session (new LLM instance)
    print("\n--- Session 2 (New Instance) ---")
    llm2 = create_llm()
    
    print("\n>>> User: What do you know about my interests?")
    response = llm2.chat("What do you know about my interests?")
    print(f">>> Assistant: {response}")


def example_with_metadata():
    """Example of using metadata with conversations."""
    print("\n" + "=" * 60)
    print("Example 3: Using Metadata")
    print("=" * 60)
    
    llm = create_llm()
    
    # Add conversation with metadata
    print("\n>>> User: Remember this important fact: Project deadline is December 15th.")
    response = llm.chat(
        "Remember this important fact: Project deadline is December 15th.",
        metadata={"type": "important", "category": "deadline"}
    )
    print(f">>> Assistant: {response}")
    
    print("\n>>> User: What important deadlines do I have?")
    response = llm.chat("What important deadlines do I have?")
    print(f">>> Assistant: {response}")


def example_clear_memory():
    """Example of clearing memory."""
    print("\n" + "=" * 60)
    print("Example 4: Clearing Memory")
    print("=" * 60)
    
    llm = create_llm()
    
    print("\n>>> User: My favorite color is blue.")
    response = llm.chat("My favorite color is blue.")
    print(f">>> Assistant: {response}")
    
    # Clear only short-term memory
    print("\n>>> Clearing short-term memory...")
    llm.clear_memory(clear_long_term=False)
    
    print("\n>>> User: What's my favorite color?")
    response = llm.chat("What's my favorite color?")
    print(f">>> Assistant: {response}")
    print("(Should still remember from long-term memory)")


def interactive_mode():
    """Interactive chat mode."""
    print("\n" + "=" * 60)
    print("Interactive Mode")
    print("=" * 60)
    print("Type 'exit' to quit, 'clear' to clear short-term memory")
    print("Type 'stats' to see memory statistics")
    print("=" * 60)
    
    llm = create_llm()
    
    while True:
        try:
            user_input = input("\n>>> You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            
            if user_input.lower() == 'clear':
                llm.clear_memory(clear_long_term=False)
                print("Short-term memory cleared!")
                continue
            
            if user_input.lower() == 'stats':
                stats = llm.get_memory_stats()
                print(f"Memory Stats: {stats}")
                continue
            
            response = llm.chat(user_input)
            print(f">>> Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


def main():
    """Run all examples."""
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("=" * 60)
        print("WARNING: OPENAI_API_KEY not set!")
        print("=" * 60)
        print("Please set your OpenAI API key:")
        print("1. Copy .env.example to .env")
        print("2. Add your API key to .env")
        print("3. Run this script again")
        print("=" * 60)
        return
    
    print("Professional LangChain LLM - Example Usage")
    print("=" * 60)
    
    # Run examples
    try:
        example_basic_conversation()
        example_memory_persistence()
        example_with_metadata()
        example_clear_memory()
        
        # Ask if user wants interactive mode
        print("\n" + "=" * 60)
        choice = input("Would you like to enter interactive mode? (y/n): ").strip().lower()
        if choice == 'y':
            interactive_mode()
    
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("\nPlease make sure:")
        print("1. Your OpenAI API key is set correctly")
        print("2. You have installed all dependencies: pip install -r requirements.txt")


if __name__ == "__main__":
    main()
