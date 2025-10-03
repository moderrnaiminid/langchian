#!/usr/bin/env python3
"""
Quick validation script to test module structure without requiring API keys.
This script verifies that all components are properly structured.
"""
import sys


def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")
    
    # We can't import modules that depend on external packages
    # So we'll just verify the syntax is valid
    import ast
    
    modules = ['config.py', 'memory_manager.py', 'llm_app.py', 'example.py']
    
    try:
        for module in modules:
            with open(module, 'r') as f:
                ast.parse(f.read())
            print(f"✓ {module} has valid Python syntax")
        
        print("✓ All core modules have valid structure")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in {module}: {e}")
        return False
    except Exception as e:
        print(f"✗ Failed to validate modules: {e}")
        return False


def test_config_structure():
    """Test configuration structure."""
    print("\nTesting configuration structure...")
    
    try:
        # Read config file and check structure
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Check for key class and attributes
        required_items = [
            'class Config',
            'OPENAI_API_KEY',
            'MODEL_NAME',
            'TEMPERATURE',
            'MAX_TOKENS',
            'def validate'
        ]
        
        all_present = True
        for item in required_items:
            if item in content:
                print(f"✓ Config has '{item}'")
            else:
                print(f"✗ Config missing '{item}'")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    import os
    required_files = [
        'config.py',
        'memory_manager.py',
        'llm_app.py',
        'example.py',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            all_exist = False
    
    return all_exist


def test_requirements():
    """Test requirements.txt content."""
    print("\nTesting requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_packages = [
            'langchain',
            'chromadb',
            'openai',
            'python-dotenv'
        ]
        
        all_present = True
        for package in required_packages:
            if package in content:
                print(f"✓ {package} in requirements")
            else:
                print(f"✗ {package} missing from requirements")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"✗ Failed to read requirements.txt: {e}")
        return False


def test_readme():
    """Test README.md content."""
    print("\nTesting README.md...")
    
    try:
        with open('README.md', 'r') as f:
            content = f.read()
        
        required_sections = [
            'Installation',
            'Configuration',
            'Usage',
            'Architecture',
            'Features'
        ]
        
        all_present = True
        for section in required_sections:
            if section in content:
                print(f"✓ {section} section present")
            else:
                print(f"✗ {section} section missing")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"✗ Failed to read README.md: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("LangChain Professional LLM - Structure Validation")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config_structure),
        ("File Structure", test_file_structure),
        ("Requirements", test_requirements),
        ("Documentation", test_readme)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All validation tests passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up .env file with your OpenAI API key")
        print("3. Run examples: python example.py")
        return 0
    else:
        print("\n✗ Some validation tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
