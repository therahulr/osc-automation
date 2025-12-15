# Gemini API Integration

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Add API key to .env
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

Get your API key from: https://ai.google.dev/

### 2. Basic Usage

```python
from core import create_gemini_client

# Create client
client = create_gemini_client()

# Generate text
response = client.generate_text("Explain test automation")
print(response.text)

# Process document
response = client.process_document(
    file_path="test_plan.pdf",
    prompt="Summarize this test plan"
)
print(response.text)

# Analyze screenshot
response = client.analyze_screenshot(
    screenshot_path="error.png",
    prompt="What error is shown?"
)
print(response.text)
```

## Features

✅ **Text Generation** - Generate test cases, documentation, scripts  
✅ **Document Processing** - PDF, Word, Excel, images  
✅ **Screenshot Analysis** - Analyze UI errors and bugs  
✅ **Test Case Extraction** - Extract test cases from documents  
✅ **Bug Report Creation** - Generate structured bug reports  
✅ **Test Result Analysis** - Analyze and summarize test results  
✅ **Multimodal Support** - Process text, images, and documents together  

## Supported File Types

| Category | Formats |
|----------|---------|
| **Images** | JPG, PNG, GIF, WebP, BMP |
| **Documents** | PDF, TXT, CSV, JSON, XML, HTML, Markdown |
| **Office** | Excel (XLSX, XLS), Word (DOCX, DOC), PowerPoint (PPTX, PPT) |

## Common Use Cases

### Extract Test Cases

```python
response = client.extract_test_cases(
    document_path="requirements.pdf"
)
```

### Create Bug Report

```python
response = client.create_bug_report(
    description="Login button not working",
    screenshot_path="bug.png"
)
```

### Analyze Test Results

```python
response = client.analyze_test_results(
    results_file="test_results.csv"
)
```

### Compare Documents

```python
response = client.process_multiple_documents(
    file_paths=["v1.pdf", "v2.pdf"],
    prompt="What changed between versions?"
)
```

## Configuration

Environment variables in `.env`:

```bash
GEMINI_API_KEY=your_key_here          # Required
GEMINI_MODEL=gemini-2.5-flash         # Optional (default)
GEMINI_TEMPERATURE=0.7                # Optional (0.0-1.0)
GEMINI_MAX_TOKENS=8192                # Optional
```

## Examples

Run the examples:

```bash
python examples/gemini_client_examples.py
```

## Documentation

Full documentation: [docs/gemini_client.md](docs/gemini_client.md)

## Models

- **gemini-2.5-flash** - Fast, efficient (recommended)
- **gemini-2.5-pro** - More capable for complex tasks
- **gemini-1.5-flash** - Previous generation, fast
- **gemini-1.5-pro** - Previous generation, capable

## Error Handling

Always check response status:

```python
response = client.generate_text("...")

if response.success:
    print(response.text)
else:
    print(f"Error: {response.error}")
```

## Best Practices

1. **Be specific in prompts** - Clear instructions get better results
2. **Use system instructions** - Guide the model's behavior
3. **Handle errors gracefully** - Check `response.success`
4. **Optimize costs** - Use appropriate model and token limits
5. **Add delays for batch processing** - Avoid rate limits

## Troubleshooting

### API Key Not Found
```bash
# Add to .env file
GEMINI_API_KEY=your_actual_key
```

### File Not Supported
Check supported formats above. Convert if needed.

### Rate Limit
Add delays between requests or upgrade quota.

## Integration Example

```python
from core import UIAutomationCore, create_gemini_client

class SmartTestRunner:
    def __init__(self):
        self.gemini = create_gemini_client()
    
    def analyze_failure(self, screenshot_path, error_log):
        """Analyze test failure with AI."""
        prompt = f"""
        Test failed with error:
        {error_log}
        
        Suggest:
        1. Root cause
        2. How to fix
        3. Prevention strategy
        """
        
        return self.gemini.analyze_screenshot(
            screenshot_path=screenshot_path,
            prompt=prompt
        )
    
    def generate_test_cases(self, feature_description):
        """Generate test cases from feature description."""
        return self.gemini.generate_text(
            prompt=f"Generate comprehensive test cases for: {feature_description}",
            system_instruction="You are a senior QA engineer"
        )
```

## Resources

- [Official Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Get API Key](https://ai.google.dev/)
- [Full Documentation](docs/gemini_client.md)
- [Examples](examples/gemini_client_examples.py)

## Support

For issues or questions:
1. Check [documentation](docs/gemini_client.md)
2. Review [examples](examples/gemini_client_examples.py)
3. Check official Gemini docs
4. Contact automation team
