"""Example usage of the Gemini API client.

This script demonstrates various use cases for the Gemini client including:
- Text generation
- Document processing
- Screenshot analysis
- Test case extraction
- Bug report creation
- Test result analysis
"""

from pathlib import Path
from core.gemini_client import create_gemini_client, GeminiClient
from core.logger import logger


def example_text_generation():
    """Example: Generate text from a prompt."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Text Generation")
    print("="*80)
    
    client = create_gemini_client()
    
    # Simple text generation
    response = client.generate_text(
        prompt="Explain the importance of test automation in 3 bullet points."
    )
    
    if response.success:
        print("\nGenerated Response:")
        print(response.text)
    else:
        print(f"\nError: {response.error}")


def example_text_generation_with_system_instruction():
    """Example: Generate text with system instruction."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Text Generation with System Instruction")
    print("="*80)
    
    client = create_gemini_client()
    
    response = client.generate_text(
        prompt="Write a test case for user login functionality",
        system_instruction="You are an experienced QA engineer. Write detailed, professional test cases following industry best practices."
    )
    
    if response.success:
        print("\nGenerated Test Case:")
        print(response.text)
    else:
        print(f"\nError: {response.error}")


def example_document_processing():
    """Example: Process a PDF document."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Document Processing")
    print("="*80)
    
    client = create_gemini_client()
    
    # Example with a PDF file (replace with actual file path)
    pdf_path = "path/to/your/document.pdf"
    
    if Path(pdf_path).exists():
        response = client.process_document(
            file_path=pdf_path,
            prompt="Summarize this document in 5 key points."
        )
        
        if response.success:
            print("\nDocument Summary:")
            print(response.text)
        else:
            print(f"\nError: {response.error}")
    else:
        print(f"\nSkipping: File not found: {pdf_path}")
        print("To test this, provide a valid PDF file path.")


def example_screenshot_analysis():
    """Example: Analyze a screenshot."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Screenshot Analysis")
    print("="*80)
    
    client = create_gemini_client()
    
    # Example with a screenshot (replace with actual file path)
    screenshot_path = "path/to/screenshot.png"
    
    if Path(screenshot_path).exists():
        response = client.analyze_screenshot(
            screenshot_path=screenshot_path,
            prompt="Describe what you see in this screenshot. Identify any errors or issues visible."
        )
        
        if response.success:
            print("\nScreenshot Analysis:")
            print(response.text)
        else:
            print(f"\nError: {response.error}")
    else:
        print(f"\nSkipping: File not found: {screenshot_path}")
        print("To test this, provide a valid screenshot file path.")


def example_test_case_extraction():
    """Example: Extract test cases from a document."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Test Case Extraction")
    print("="*80)
    
    client = create_gemini_client()
    
    # Custom template for test case extraction
    template = """
    Extract all test cases from this document and format them as JSON with the following structure:
    
    {
        "test_cases": [
            {
                "id": "TC-001",
                "title": "Test case title",
                "description": "Brief description",
                "preconditions": ["condition 1", "condition 2"],
                "steps": [
                    {"step": 1, "action": "action description", "expected": "expected result"}
                ],
                "priority": "High/Medium/Low",
                "tags": ["tag1", "tag2"]
            }
        ]
    }
    
    Be thorough and extract all test cases you can find.
    """
    
    document_path = "path/to/test_cases.pdf"
    
    if Path(document_path).exists():
        response = client.extract_test_cases(
            document_path=document_path,
            template=template
        )
        
        if response.success:
            print("\nExtracted Test Cases:")
            print(response.text)
        else:
            print(f"\nError: {response.error}")
    else:
        print(f"\nSkipping: File not found: {document_path}")
        print("To test this, provide a valid document with test cases.")


def example_bug_report_creation():
    """Example: Create a bug report."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Bug Report Creation")
    print("="*80)
    
    client = create_gemini_client()
    
    # Create bug report from description
    bug_description = """
    When trying to submit a loan application form, clicking the Submit button
    does nothing. The button appears to be clickable but no action occurs.
    This happens in Chrome browser on macOS. The console shows a JavaScript
    error: "Cannot read property 'validate' of undefined".
    """
    
    response = client.create_bug_report(
        description=bug_description,
        screenshot_path=None  # Can add screenshot path if available
    )
    
    if response.success:
        print("\nGenerated Bug Report:")
        print(response.text)
    else:
        print(f"\nError: {response.error}")


def example_bug_report_with_screenshot():
    """Example: Create a bug report with screenshot."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Bug Report with Screenshot")
    print("="*80)
    
    client = create_gemini_client()
    
    bug_description = "Application crashes when uploading large files"
    screenshot_path = "path/to/error_screenshot.png"
    
    if Path(screenshot_path).exists():
        response = client.create_bug_report(
            description=bug_description,
            screenshot_path=screenshot_path
        )
        
        if response.success:
            print("\nGenerated Bug Report with Screenshot Analysis:")
            print(response.text)
        else:
            print(f"\nError: {response.error}")
    else:
        print(f"\nSkipping: File not found: {screenshot_path}")
        print("To test this, provide a valid screenshot file path.")


def example_test_results_analysis():
    """Example: Analyze test results."""
    print("\n" + "="*80)
    print("EXAMPLE 8: Test Results Analysis")
    print("="*80)
    
    client = create_gemini_client()
    
    results_file = "path/to/test_results.csv"  # Can be CSV, Excel, JSON, etc.
    
    if Path(results_file).exists():
        response = client.analyze_test_results(results_file)
        
        if response.success:
            print("\nTest Results Analysis:")
            print(response.text)
        else:
            print(f"\nError: {response.error}")
    else:
        print(f"\nSkipping: File not found: {results_file}")
        print("To test this, provide a valid test results file.")


def example_multiple_documents():
    """Example: Process multiple documents together."""
    print("\n" + "="*80)
    print("EXAMPLE 9: Multiple Document Processing")
    print("="*80)
    
    client = create_gemini_client()
    
    documents = [
        "path/to/test_plan_v1.pdf",
        "path/to/test_plan_v2.pdf"
    ]
    
    # Check if files exist
    existing_docs = [doc for doc in documents if Path(doc).exists()]
    
    if len(existing_docs) >= 2:
        response = client.process_multiple_documents(
            file_paths=existing_docs,
            prompt="Compare these test plans and identify the key differences between them."
        )
        
        if response.success:
            print("\nComparison Results:")
            print(response.text)
        else:
            print(f"\nError: {response.error}")
    else:
        print(f"\nSkipping: Need at least 2 documents. Found {len(existing_docs)}.")
        print("To test this, provide paths to multiple documents.")


def example_model_info():
    """Example: Get model information."""
    print("\n" + "="*80)
    print("EXAMPLE 10: Model Information")
    print("="*80)
    
    client = create_gemini_client()
    
    # Get info about the current model
    info = client.get_model_info()
    
    print("\nCurrent Model Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # List available models
    print("\nAvailable Models:")
    models = client.list_models()
    for model in models[:10]:  # Show first 10
        print(f"  - {model}")
    if len(models) > 10:
        print(f"  ... and {len(models) - 10} more")


def example_custom_template():
    """Example: Use custom template for specific output format."""
    print("\n" + "="*80)
    print("EXAMPLE 11: Custom Template for Defect Analysis")
    print("="*80)
    
    client = create_gemini_client()
    
    # Custom template for defect categorization
    template = """
    Analyze the following bug description and categorize it:
    
    Bug: {description}
    
    Provide the analysis in this exact format:
    
    CATEGORY: [UI/Backend/Database/Integration/Performance/Security]
    SEVERITY: [Critical/High/Medium/Low]
    COMPONENT: [Specific component or module affected]
    ROOT_CAUSE: [Likely root cause based on description]
    SUGGESTED_FIX: [Recommended approach to fix]
    ESTIMATED_EFFORT: [Small/Medium/Large]
    RELATED_AREAS: [Other areas that might be affected]
    """
    
    bug_desc = "Login page takes 15 seconds to load. Database query logs show a full table scan on users table with 10M records."
    
    response = client.generate_text(
        prompt=template.format(description=bug_desc),
        system_instruction="You are a senior software engineer analyzing defects."
    )
    
    if response.success:
        print("\nDefect Analysis:")
        print(response.text)
    else:
        print(f"\nError: {response.error}")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("GEMINI API CLIENT - USAGE EXAMPLES")
    print("="*80)
    print("\nThese examples demonstrate various capabilities of the Gemini client.")
    print("Some examples require actual files - update the file paths to test them.")
    print("\nMake sure to set GEMINI_API_KEY in your .env file before running.")
    
    try:
        # Examples that don't require files
        example_text_generation()
        example_text_generation_with_system_instruction()
        example_bug_report_creation()
        example_custom_template()
        example_model_info()
        
        # Examples that require files (will skip if files don't exist)
        example_document_processing()
        example_screenshot_analysis()
        example_test_case_extraction()
        example_bug_report_with_screenshot()
        example_test_results_analysis()
        example_multiple_documents()
        
        print("\n" + "="*80)
        print("EXAMPLES COMPLETED")
        print("="*80)
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure GEMINI_API_KEY is set in your .env file.")
        print("Get your API key from: https://ai.google.dev/")
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
