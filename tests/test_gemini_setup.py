"""Quick test to verify Gemini client installation and configuration.

Run this to check if everything is set up correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path to import core modules
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    try:
        from core.gemini_client import GeminiClient, GeminiResponse, create_gemini_client
        print("✅ Gemini client imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are installed."""
    print("\nTesting dependencies...")
    try:
        import google.genai
        print("✅ google-genai installed")
    except ImportError:
        print("❌ google-genai not installed")
        return False
    
    try:
        import httpx
        print("✅ httpx installed")
    except ImportError:
        print("❌ httpx not installed")
        return False
    
    return True

def test_configuration():
    """Test if API key is configured."""
    print("\nTesting configuration...")
    try:
        from core.utils import get_env
        api_key = get_env("GEMINI_API_KEY")
        
        if not api_key:
            print("⚠️  GEMINI_API_KEY not set in .env file")
            print("   Add your API key to .env:")
            print("   GEMINI_API_KEY=your_api_key_here")
            print("   Get your key from: https://ai.google.dev/")
            return False
        elif api_key == "your_gemini_api_key_here":
            print("⚠️  GEMINI_API_KEY is set to placeholder value")
            print("   Replace with your actual API key from: https://ai.google.dev/")
            return False
        else:
            print(f"✅ GEMINI_API_KEY configured (length: {len(api_key)} chars)")
            return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_client_creation():
    """Test if client can be created."""
    print("\nTesting client creation...")
    try:
        from core.gemini_client import create_gemini_client
        
        # Try to create client (will fail if API key is not set)
        try:
            client = create_gemini_client()
            print(f"✅ Client created successfully")
            print(f"   Model: {client.model}")
            print(f"   Temperature: {client.temperature}")
            print(f"   Max Tokens: {client.max_tokens}")
            return True
        except ValueError as e:
            if "API key not found" in str(e):
                print("⚠️  Cannot create client: API key not configured")
                print("   Add GEMINI_API_KEY to your .env file")
                return False
            raise
    except Exception as e:
        print(f"❌ Client creation error: {e}")
        return False

def test_simple_request():
    """Test a simple API request (only if API key is configured)."""
    print("\nTesting simple API request...")
    try:
        from core.gemini_client import create_gemini_client
        
        client = create_gemini_client()
        
        print("   Sending test request to Gemini API...")
        response = client.generate_text(
            prompt="Say 'Hello from Gemini!' in exactly 3 words.",
            max_tokens=50
        )
        
        if response.success:
            print(f"✅ API request successful!")
            print(f"   Response: {response.text}")
            return True
        else:
            print(f"❌ API request failed: {response.error}")
            return False
            
    except ValueError as e:
        if "API key not found" in str(e):
            print("⚠️  Skipping API test: API key not configured")
            return None  # Not a failure, just skipped
        raise
    except Exception as e:
        print(f"❌ API request error: {e}")
        return False

def main():
    """Run all tests."""
    print("="*80)
    print("GEMINI CLIENT - INSTALLATION VERIFICATION")
    print("="*80)
    
    results = {
        "imports": test_imports(),
        "dependencies": test_dependencies(),
        "configuration": test_configuration(),
        "client_creation": test_client_creation(),
        "api_request": test_simple_request()
    }
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, result in results.items():
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⚠️  SKIP"
        print(f"{test_name.replace('_', ' ').title():.<40} {status}")
    
    print("="*80)
    
    # Overall status
    failed_tests = [name for name, result in results.items() if result is False]
    skipped_tests = [name for name, result in results.items() if result is None]
    
    if not failed_tests:
        if skipped_tests:
            print("\n✅ All tests passed (some skipped)")
            print("\nTo enable skipped tests:")
            print("1. Add your GEMINI_API_KEY to .env file")
            print("2. Get your key from: https://ai.google.dev/")
        else:
            print("\n🎉 All tests passed! Gemini client is ready to use.")
    else:
        print(f"\n❌ {len(failed_tests)} test(s) failed: {', '.join(failed_tests)}")
        print("\nPlease fix the issues above before using the Gemini client.")
        sys.exit(1)
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("1. If not done, add GEMINI_API_KEY to .env file")
    print("2. Review documentation: docs/gemini_client.md")
    print("3. Run examples: python examples/gemini_client_examples.py")
    print("4. Start integrating into your automation workflows!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
