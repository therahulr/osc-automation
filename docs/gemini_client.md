# Gemini API Client Documentation

## Overview

The Gemini API client provides a comprehensive interface for integrating Google's Gemini AI models into the automation framework. It supports text generation, multimodal document processing, and specialized automation tasks.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [Features](#features)
- [API Reference](#api-reference)
- [Use Cases](#use-cases)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `google-genai>=1.0.0` - Official Google Gemini SDK
- `httpx>=0.25.0` - HTTP client for document fetching

### 2. Get API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

### 3. Configure Environment

Add to your `.env` file:

```bash
# Gemini API Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=8192
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Your Gemini API key | - | ✅ Yes |
| `GEMINI_MODEL` | Model to use | `gemini-2.5-flash` | ❌ No |
| `GEMINI_TEMPERATURE` | Creativity level (0.0-1.0) | `0.7` | ❌ No |
| `GEMINI_MAX_TOKENS` | Max output tokens | `8192` | ❌ No |

### Available Models

- **gemini-2.5-flash** - Fast, efficient, good for most tasks (recommended)
- **gemini-2.5-pro** - More capable, better for complex tasks
- **gemini-1.5-flash** - Previous generation, fast
- **gemini-1.5-pro** - Previous generation, capable

### Temperature Settings

- **0.0-0.3**: Deterministic, factual responses
- **0.4-0.7**: Balanced creativity and consistency (recommended)
- **0.8-1.0**: More creative, varied responses

## Quick Start

### Basic Text Generation

```python
from core.gemini_client import create_gemini_client

# Create client
client = create_gemini_client()

# Generate text
response = client.generate_text("Explain test automation in 3 points")

if response.success:
    print(response.text)
else:
    print(f"Error: {response.error}")
```

### Process a Document

```python
# Process PDF, Word, Excel, or image
response = client.process_document(
    file_path="test_plan.pdf",
    prompt="Summarize this test plan"
)

print(response.text)
```

### Analyze Screenshot

```python
response = client.analyze_screenshot(
    screenshot_path="error.png",
    prompt="What error is shown? How to fix it?"
)

print(response.text)
```

## Features

### 1. Text Generation

Generate text from prompts with optional system instructions.

```python
response = client.generate_text(
    prompt="Write a test case for login",
    system_instruction="You are a QA engineer",
    temperature=0.5,
    max_tokens=2048
)
```

### 2. Document Processing

Process various document types:

#### Supported Formats

**Images:**
- JPEG/JPG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- GIF (`.gif`)
- WebP (`.webp`)
- BMP (`.bmp`)

**Documents:**
- PDF (`.pdf`)
- Text (`.txt`)
- CSV (`.csv`)
- JSON (`.json`)
- XML (`.xml`)
- HTML (`.html`)
- Markdown (`.md`)

**Office Files:**
- Excel (`.xlsx`, `.xls`)
- Word (`.docx`, `.doc`)
- PowerPoint (`.pptx`, `.ppt`)

#### Single Document

```python
response = client.process_document(
    file_path="document.pdf",
    prompt="Extract key information"
)
```

#### Multiple Documents

```python
response = client.process_multiple_documents(
    file_paths=["doc1.pdf", "doc2.pdf"],
    prompt="Compare these documents"
)
```

### 3. Specialized Methods

#### Extract Test Cases

```python
response = client.extract_test_cases(
    document_path="test_cases.pdf",
    template=None  # Uses default template
)
```

Default output includes:
- Test Case ID
- Title/Name
- Description
- Preconditions
- Test Steps
- Expected Results
- Priority
- Tags/Labels

#### Create Bug Report

```python
# Without screenshot
response = client.create_bug_report(
    description="Login button not working",
    screenshot_path=None
)

# With screenshot
response = client.create_bug_report(
    description="Error on submit",
    screenshot_path="error.png"
)
```

#### Analyze Test Results

```python
response = client.analyze_test_results(
    results_file="test_results.csv"
)
```

Provides:
- Summary statistics
- Failed test analysis
- Common patterns
- Recommendations

### 4. Model Information

```python
# Get current model info
info = client.get_model_info()
print(info)

# List available models
models = client.list_models()
for model in models:
    print(model)
```

## API Reference

### GeminiClient Class

#### Constructor

```python
GeminiClient(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
)
```

#### Methods

##### generate_text()

```python
generate_text(
    prompt: str,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    system_instruction: Optional[str] = None
) -> GeminiResponse
```

Generate text from a prompt.

**Parameters:**
- `prompt`: The text prompt
- `model`: Override default model
- `temperature`: Override default temperature
- `max_tokens`: Override default max tokens
- `system_instruction`: System instruction to guide the model

**Returns:** `GeminiResponse` object

##### process_document()

```python
process_document(
    file_path: Union[str, Path],
    prompt: str,
    model: Optional[str] = None,
    use_file_api: bool = False
) -> GeminiResponse
```

Process a document with a prompt.

**Parameters:**
- `file_path`: Path to document
- `prompt`: Question/instruction about the document
- `model`: Override default model
- `use_file_api`: Force use of File API for large files

**Returns:** `GeminiResponse` object

##### process_multiple_documents()

```python
process_multiple_documents(
    file_paths: List[Union[str, Path]],
    prompt: str,
    model: Optional[str] = None
) -> GeminiResponse
```

Process multiple documents together.

##### analyze_screenshot()

```python
analyze_screenshot(
    screenshot_path: Union[str, Path],
    prompt: str = "Describe what you see in this screenshot in detail.",
    model: Optional[str] = None
) -> GeminiResponse
```

Analyze a screenshot image.

##### extract_test_cases()

```python
extract_test_cases(
    document_path: Union[str, Path],
    template: Optional[str] = None
) -> GeminiResponse
```

Extract test cases from a document.

##### create_bug_report()

```python
create_bug_report(
    description: str,
    screenshot_path: Optional[Union[str, Path]] = None,
    template: Optional[str] = None
) -> GeminiResponse
```

Create a structured bug report.

##### analyze_test_results()

```python
analyze_test_results(
    results_file: Union[str, Path],
    template: Optional[str] = None
) -> GeminiResponse
```

Analyze test results and provide summary.

### GeminiResponse Class

```python
@dataclass
class GeminiResponse:
    text: str                    # Generated text
    raw_response: Any           # Raw API response
    model: str                  # Model used
    success: bool = True        # Success status
    error: Optional[str] = None # Error message if failed
```

## Use Cases

### 1. Test Case Management

#### Extract Test Cases from Documents

```python
client = create_gemini_client()

response = client.extract_test_cases(
    document_path="requirements.pdf",
    template="""
    Extract test cases and format as JSON:
    {
        "test_cases": [
            {
                "id": "TC-001",
                "title": "...",
                "steps": [...],
                "expected": "..."
            }
        ]
    }
    """
)
```

#### Generate Test Cases from Requirements

```python
response = client.generate_text(
    prompt="Generate test cases for user registration feature with email verification",
    system_instruction="You are a QA engineer. Create comprehensive test cases."
)
```

### 2. Bug Tracking

#### Analyze Bug Screenshots

```python
response = client.analyze_screenshot(
    screenshot_path="bug_screenshot.png",
    prompt="""
    Analyze this bug:
    1. What error is shown?
    2. What might be the cause?
    3. How to reproduce?
    4. Suggested fix?
    """
)
```

#### Create Structured Bug Reports

```python
response = client.create_bug_report(
    description="Application crashes when uploading files > 10MB",
    screenshot_path="crash_screenshot.png"
)
```

### 3. Test Result Analysis

#### Analyze Test Reports

```python
response = client.analyze_test_results(
    results_file="test_results.xlsx",
    template="""
    Analyze test results:
    1. Pass/fail statistics
    2. Flaky tests
    3. Common failure patterns
    4. Priority areas for investigation
    """
)
```

### 4. Documentation Processing

#### Compare Test Plans

```python
response = client.process_multiple_documents(
    file_paths=["test_plan_v1.pdf", "test_plan_v2.pdf"],
    prompt="What are the key differences between these test plans?"
)
```

#### Extract Information from Excel

```python
response = client.process_document(
    file_path="test_data.xlsx",
    prompt="Extract all test scenarios with priority 'High'"
)
```

### 5. Automation Script Generation

```python
response = client.generate_text(
    prompt="""
    Generate a Playwright automation script for:
    1. Navigate to login page
    2. Enter credentials
    3. Click login button
    4. Verify dashboard loads
    """,
    system_instruction="You are an automation engineer. Write clean, maintainable code."
)
```

## Best Practices

### 1. Prompt Engineering

#### Be Specific

❌ Bad:
```python
prompt = "Analyze this"
```

✅ Good:
```python
prompt = "Analyze this test report and identify: 1) Total pass/fail count, 2) Most common failure reasons, 3) Flaky tests"
```

#### Use System Instructions

```python
response = client.generate_text(
    prompt="Write test cases for login",
    system_instruction="You are a senior QA engineer with 10 years experience. Write detailed, professional test cases following IEEE standards."
)
```

#### Provide Context

```python
prompt = """
Context: We're testing a banking application's fund transfer feature.
Requirements: User must be logged in, have sufficient balance, and recipient must be valid.

Task: Generate negative test cases for this feature.
"""
```

### 2. File Handling

#### Small Files (< 20MB)

Use inline data (automatic):
```python
response = client.process_document(
    file_path="small_doc.pdf",
    prompt="Summarize"
)
```

#### Large Files (> 20MB)

Force File API usage:
```python
response = client.process_document(
    file_path="large_doc.pdf",
    prompt="Summarize",
    use_file_api=True
)
```

### 3. Error Handling

Always check response status:

```python
response = client.generate_text("...")

if response.success:
    # Process the result
    print(response.text)
else:
    # Handle the error
    logger.error(f"Gemini API error: {response.error}")
    # Fallback logic
```

### 4. Rate Limiting

Implement delays for batch processing:

```python
import time

for document in documents:
    response = client.process_document(document, prompt)
    # Process response
    time.sleep(1)  # Avoid rate limits
```

### 5. Cost Optimization

#### Use Appropriate Models

- **gemini-2.5-flash**: Fast, cost-effective for most tasks
- **gemini-2.5-pro**: Use only for complex tasks requiring higher quality

#### Optimize Token Usage

```python
# Be concise in prompts
response = client.generate_text(
    prompt="List 3 key test scenarios for login",
    max_tokens=500  # Limit output
)
```

## Troubleshooting

### Common Issues

#### 1. API Key Not Found

**Error:** `ValueError: Gemini API key not found`

**Solution:**
```bash
# Add to .env file
GEMINI_API_KEY=your_actual_api_key_here
```

#### 2. File Not Supported

**Error:** `ValueError: Unsupported file type: .xyz`

**Solution:** Check supported file types in documentation. Convert file to supported format.

#### 3. File Too Large

**Error:** File upload fails for large files

**Solution:**
```python
# Use File API for large files
response = client.process_document(
    file_path="large_file.pdf",
    prompt="...",
    use_file_api=True
)
```

#### 4. Rate Limit Exceeded

**Error:** API returns rate limit error

**Solution:**
- Add delays between requests
- Implement exponential backoff
- Consider upgrading API quota

#### 5. Empty Response

**Issue:** `response.text` is empty

**Possible Causes:**
- Prompt is unclear
- Content filtered by safety settings
- Model couldn't generate relevant response

**Solution:**
- Rephrase prompt
- Check `response.raw_response` for details
- Try different model

### Debug Mode

Enable detailed logging:

```python
from core.logger import logger
import logging

logger.setLevel(logging.DEBUG)

# Now all API calls will log detailed information
client = create_gemini_client()
response = client.generate_text("...")
```

### Getting Help

1. Check the [official Gemini API documentation](https://ai.google.dev/gemini-api/docs)
2. Review example code in `examples/gemini_client_examples.py`
3. Check logs in `logs/` directory
4. Enable debug logging for more details

## Advanced Usage

### Custom Templates

Create reusable templates:

```python
BUG_ANALYSIS_TEMPLATE = """
Analyze this bug and provide:

BUG TITLE: [Clear, concise title]
SEVERITY: [Critical/High/Medium/Low]
COMPONENT: [Affected component]
DESCRIPTION: [Detailed description]
STEPS TO REPRODUCE:
1. [Step 1]
2. [Step 2]
...

EXPECTED: [Expected behavior]
ACTUAL: [Actual behavior]
ROOT CAUSE: [Likely cause]
FIX SUGGESTION: [How to fix]

Bug Details: {bug_description}
"""

response = client.generate_text(
    prompt=BUG_ANALYSIS_TEMPLATE.format(bug_description="...")
)
```

### Batch Processing

Process multiple items efficiently:

```python
def process_batch(items, prompt_template):
    results = []
    for item in items:
        response = client.generate_text(
            prompt=prompt_template.format(item=item)
        )
        if response.success:
            results.append(response.text)
        time.sleep(0.5)  # Rate limiting
    return results
```

### Integration with Automation

```python
from core.gemini_client import create_gemini_client

class TestAnalyzer:
    def __init__(self):
        self.gemini = create_gemini_client()
    
    def analyze_failure(self, screenshot_path, error_log):
        prompt = f"""
        Analyze this test failure:
        
        Error Log:
        {error_log}
        
        Based on the screenshot and error, suggest:
        1. Root cause
        2. How to fix
        3. How to prevent in future
        """
        
        return self.gemini.analyze_screenshot(
            screenshot_path=screenshot_path,
            prompt=prompt
        )
```

## Examples

See `examples/gemini_client_examples.py` for comprehensive examples of all features.

Run examples:
```bash
python examples/gemini_client_examples.py
```

## License

This client is part of the automation framework and follows the same license.

## Support

For issues or questions:
1. Check this documentation
2. Review examples
3. Check official Gemini API docs
4. Contact the automation team
