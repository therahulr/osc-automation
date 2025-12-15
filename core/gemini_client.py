"""Gemini API client for AI-powered automation tasks.

This module provides a comprehensive client for interacting with Google's Gemini API
to perform various AI tasks including:
- Test case identification and analysis
- Bug and defect creation
- Summary analysis
- Document processing (screenshots, Excel, Word, PDF)
- Multimodal content understanding
"""

import os
import base64
import mimetypes
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass

from google import genai
from google.genai import types

from core.logger import get_logger
from core.utils import get_env

# Initialize logger for this module
logger = get_logger("gemini_client")



@dataclass
class GeminiResponse:
    """Structured response from Gemini API.
    
    Attributes:
        text: The generated text response
        raw_response: The raw response object from the API
        model: The model used for generation
        success: Whether the request was successful
        error: Error message if request failed
    """
    text: str
    raw_response: Any
    model: str
    success: bool = True
    error: Optional[str] = None


class GeminiClient:
    """Client for interacting with Google Gemini API.
    
    This client provides methods for:
    - Text generation and analysis
    - Document processing (PDF, Word, Excel, images)
    - Multimodal content understanding
    - Template-based output generation
    
    The client automatically handles:
    - API key management from environment variables
    - File upload for large documents
    - Inline data for smaller files
    - Error handling and logging
    
    Environment Variables:
        GEMINI_API_KEY: Your Gemini API key (required)
        GEMINI_MODEL: Default model to use (default: gemini-2.5-flash)
        GEMINI_TEMPERATURE: Temperature for generation (default: 0.7)
        GEMINI_MAX_TOKENS: Maximum tokens to generate (default: 8192)
    
    Example:
        >>> client = GeminiClient()
        >>> response = client.generate_text("Explain test automation")
        >>> print(response.text)
        
        >>> # Process a document
        >>> response = client.process_document(
        ...     file_path="test_cases.pdf",
        ...     prompt="Extract all test case IDs and their descriptions"
        ... )
    """
    
    # Supported file types and their MIME types
    SUPPORTED_IMAGE_TYPES = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp'
    }
    
    SUPPORTED_DOCUMENT_TYPES = {
        '.pdf': 'application/pdf',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.html': 'text/html',
        '.md': 'text/markdown'
    }
    
    # Excel and Word files require special handling
    SUPPORTED_OFFICE_TYPES = {
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.xls': 'application/vnd.ms-excel',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.ppt': 'application/vnd.ms-powerpoint'
    }
    
    # Maximum file size for inline data (20MB as per Gemini API limits)
    MAX_INLINE_SIZE_BYTES = 20 * 1024 * 1024
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        """Initialize the Gemini client.
        
        Args:
            api_key: Gemini API key. If not provided, reads from GEMINI_API_KEY env var
            model: Model to use. If not provided, reads from GEMINI_MODEL env var
            temperature: Temperature for generation (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Raises:
            ValueError: If API key is not provided and not found in environment
        """
        # Get API key from parameter or environment
        self.api_key = api_key or get_env("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Set model and generation parameters
        self.model = model or get_env("GEMINI_MODEL", default="gemini-2.5-flash")
        self.temperature = temperature if temperature is not None else float(
            get_env("GEMINI_TEMPERATURE", default="0.7")
        )
        self.max_tokens = max_tokens or int(
            get_env("GEMINI_MAX_TOKENS", default="8192")
        )
        
        # Initialize the client
        # The client automatically uses GEMINI_API_KEY from environment if set
        os.environ["GEMINI_API_KEY"] = self.api_key
        self.client = genai.Client()
        
        logger.info(f"Gemini client initialized with model: {self.model}")
    
    def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_instruction: Optional[str] = None
    ) -> GeminiResponse:
        """Generate text from a prompt.
        
        Args:
            prompt: The text prompt to generate from
            model: Model to use (overrides default)
            temperature: Temperature for generation (overrides default)
            max_tokens: Maximum tokens to generate (overrides default)
            system_instruction: Optional system instruction to guide the model
            
        Returns:
            GeminiResponse containing the generated text and metadata
            
        Example:
            >>> response = client.generate_text(
            ...     prompt="Write a test case for login functionality",
            ...     system_instruction="You are a QA engineer writing test cases"
            ... )
        """
        try:
            model_name = model or self.model
            temp = temperature if temperature is not None else self.temperature
            max_tok = max_tokens or self.max_tokens
            
            logger.debug(f"Generating text with model: {model_name}")
            logger.debug(f"Prompt: {prompt[:100]}...")
            
            # Build generation config
            config = types.GenerateContentConfig(
                temperature=temp,
                max_output_tokens=max_tok,
                system_instruction=system_instruction
            )
            
            # Generate content
            response = self.client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )
            
            logger.info("Text generation successful")
            return GeminiResponse(
                text=response.text,
                raw_response=response,
                model=model_name,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return GeminiResponse(
                text="",
                raw_response=None,
                model=model_name,
                success=False,
                error=str(e)
            )
    
    def process_document(
        self,
        file_path: Union[str, Path],
        prompt: str,
        model: Optional[str] = None,
        use_file_api: bool = False
    ) -> GeminiResponse:
        """Process a document (PDF, Word, Excel, image, etc.) with a prompt.
        
        This method automatically handles:
        - File type detection
        - Choosing between inline data and File API based on size
        - Reading and encoding the file
        
        Args:
            file_path: Path to the document file
            prompt: The prompt/question about the document
            model: Model to use (overrides default)
            use_file_api: Force use of File API even for small files
            
        Returns:
            GeminiResponse containing the analysis results
            
        Example:
            >>> # Analyze a PDF document
            >>> response = client.process_document(
            ...     file_path="test_plan.pdf",
            ...     prompt="Extract all test case IDs and their priorities"
            ... )
            
            >>> # Analyze a screenshot
            >>> response = client.process_document(
            ...     file_path="bug_screenshot.png",
            ...     prompt="Describe the error shown in this screenshot"
            ... )
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Get file info
            file_size = file_path.stat().st_size
            mime_type = self._get_mime_type(file_path)
            
            logger.info(f"Processing document: {file_path.name}")
            logger.debug(f"File size: {file_size} bytes, MIME type: {mime_type}")
            
            model_name = model or self.model
            
            # Decide whether to use File API or inline data
            if use_file_api or file_size > self.MAX_INLINE_SIZE_BYTES:
                logger.debug("Using File API for large file")
                return self._process_with_file_api(file_path, prompt, model_name, mime_type)
            else:
                logger.debug("Using inline data for small file")
                return self._process_with_inline_data(file_path, prompt, model_name, mime_type)
                
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return GeminiResponse(
                text="",
                raw_response=None,
                model=model or self.model,
                success=False,
                error=str(e)
            )
    
    def process_multiple_documents(
        self,
        file_paths: List[Union[str, Path]],
        prompt: str,
        model: Optional[str] = None
    ) -> GeminiResponse:
        """Process multiple documents together with a prompt.
        
        Useful for comparing documents, finding patterns across files, etc.
        
        Args:
            file_paths: List of paths to document files
            prompt: The prompt/question about the documents
            model: Model to use (overrides default)
            
        Returns:
            GeminiResponse containing the analysis results
            
        Example:
            >>> response = client.process_multiple_documents(
            ...     file_paths=["test_v1.pdf", "test_v2.pdf"],
            ...     prompt="Compare these test plans and identify differences"
            ... )
        """
        try:
            model_name = model or self.model
            contents = []
            
            # Add all documents
            for file_path in file_paths:
                file_path = Path(file_path)
                if not file_path.exists():
                    logger.warning(f"File not found, skipping: {file_path}")
                    continue
                
                mime_type = self._get_mime_type(file_path)
                
                # Read file data
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                
                # Add as part
                contents.append(
                    types.Part.from_bytes(
                        data=file_data,
                        mime_type=mime_type
                    )
                )
                logger.debug(f"Added document: {file_path.name}")
            
            # Add prompt
            contents.append(prompt)
            
            logger.info(f"Processing {len(file_paths)} documents together")
            
            # Generate content
            response = self.client.models.generate_content(
                model=model_name,
                contents=contents
            )
            
            logger.info("Multiple document processing successful")
            return GeminiResponse(
                text=response.text,
                raw_response=response,
                model=model_name,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error processing multiple documents: {str(e)}")
            return GeminiResponse(
                text="",
                raw_response=None,
                model=model or self.model,
                success=False,
                error=str(e)
            )
    
    def analyze_screenshot(
        self,
        screenshot_path: Union[str, Path],
        prompt: str = "Describe what you see in this screenshot in detail.",
        model: Optional[str] = None
    ) -> GeminiResponse:
        """Analyze a screenshot image.
        
        Convenience method for processing screenshots with vision capabilities.
        
        Args:
            screenshot_path: Path to the screenshot image
            prompt: The prompt/question about the screenshot
            model: Model to use (overrides default)
            
        Returns:
            GeminiResponse containing the analysis
            
        Example:
            >>> response = client.analyze_screenshot(
            ...     screenshot_path="error_page.png",
            ...     prompt="What error is displayed? Suggest how to fix it."
            ... )
        """
        return self.process_document(screenshot_path, prompt, model)
    
    def extract_test_cases(
        self,
        document_path: Union[str, Path],
        template: Optional[str] = None
    ) -> GeminiResponse:
        """Extract test cases from a document.
        
        Args:
            document_path: Path to document containing test cases
            template: Optional template for output format
            
        Returns:
            GeminiResponse containing extracted test cases
        """
        default_template = """
        Extract all test cases from this document and format them as follows:
        
        For each test case, provide:
        - Test Case ID
        - Title/Name
        - Description
        - Preconditions
        - Test Steps
        - Expected Results
        - Priority
        - Tags/Labels
        
        Format the output as structured JSON.
        """
        
        prompt = template or default_template
        return self.process_document(document_path, prompt)
    
    def create_bug_report(
        self,
        description: str,
        screenshot_path: Optional[Union[str, Path]] = None,
        template: Optional[str] = None
    ) -> GeminiResponse:
        """Create a structured bug report from a description and optional screenshot.
        
        Args:
            description: Description of the bug
            screenshot_path: Optional path to screenshot showing the bug
            template: Optional template for bug report format
            
        Returns:
            GeminiResponse containing the structured bug report
        """
        default_template = """
        Based on the provided information, create a detailed bug report with:
        
        - Title: Clear, concise bug title
        - Description: Detailed description of the issue
        - Steps to Reproduce: Step-by-step instructions
        - Expected Behavior: What should happen
        - Actual Behavior: What actually happens
        - Severity: Critical/High/Medium/Low
        - Environment: Browser, OS, etc. (if mentioned)
        - Additional Notes: Any other relevant information
        
        Bug Description:
        {description}
        """
        
        prompt = (template or default_template).format(description=description)
        
        if screenshot_path:
            return self.process_document(screenshot_path, prompt)
        else:
            return self.generate_text(prompt)
    
    def analyze_test_results(
        self,
        results_file: Union[str, Path],
        template: Optional[str] = None
    ) -> GeminiResponse:
        """Analyze test results and provide summary.
        
        Args:
            results_file: Path to test results file (Excel, CSV, JSON, etc.)
            template: Optional template for analysis format
            
        Returns:
            GeminiResponse containing the analysis
        """
        default_template = """
        Analyze these test results and provide:
        
        1. Summary Statistics:
           - Total tests
           - Passed/Failed/Skipped counts
           - Pass rate percentage
        
        2. Failed Tests Analysis:
           - List of failed tests
           - Common failure patterns
           - Potential root causes
        
        3. Recommendations:
           - Areas needing attention
           - Suggested improvements
           - Priority fixes
        
        Format the output in a clear, structured manner.
        """
        
        prompt = template or default_template
        return self.process_document(results_file, prompt)
    
    def _get_mime_type(self, file_path: Path) -> str:
        """Get MIME type for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            MIME type string
            
        Raises:
            ValueError: If file type is not supported
        """
        suffix = file_path.suffix.lower()
        
        # Check our supported types first
        all_types = {
            **self.SUPPORTED_IMAGE_TYPES,
            **self.SUPPORTED_DOCUMENT_TYPES,
            **self.SUPPORTED_OFFICE_TYPES
        }
        
        if suffix in all_types:
            return all_types[suffix]
        
        # Try mimetypes module as fallback
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type:
            logger.warning(f"Using fallback MIME type for {suffix}: {mime_type}")
            return mime_type
        
        raise ValueError(
            f"Unsupported file type: {suffix}. "
            f"Supported types: {', '.join(all_types.keys())}"
        )
    
    def _process_with_inline_data(
        self,
        file_path: Path,
        prompt: str,
        model: str,
        mime_type: str
    ) -> GeminiResponse:
        """Process document using inline data.
        
        Used for smaller files (< 20MB).
        """
        try:
            # Read file data
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Create content with file and prompt
            contents = [
                types.Part.from_bytes(
                    data=file_data,
                    mime_type=mime_type
                ),
                prompt
            ]
            
            # Generate content
            response = self.client.models.generate_content(
                model=model,
                contents=contents
            )
            
            logger.info(f"Document processed successfully: {file_path.name}")
            return GeminiResponse(
                text=response.text,
                raw_response=response,
                model=model,
                success=True
            )
            
        except Exception as e:
            raise Exception(f"Error processing with inline data: {str(e)}")
    
    def _process_with_file_api(
        self,
        file_path: Path,
        prompt: str,
        model: str,
        mime_type: str
    ) -> GeminiResponse:
        """Process document using File API.
        
        Used for larger files (> 20MB) or when explicitly requested.
        Files are uploaded to Gemini and stored for 48 hours.
        """
        try:
            logger.info(f"Uploading file to Gemini: {file_path.name}")
            
            # Upload file
            uploaded_file = self.client.files.upload(file=str(file_path))
            
            logger.debug(f"File uploaded with URI: {uploaded_file.uri}")
            
            # Generate content using uploaded file
            response = self.client.models.generate_content(
                model=model,
                contents=[uploaded_file, prompt]
            )
            
            logger.info(f"Document processed successfully: {file_path.name}")
            return GeminiResponse(
                text=response.text,
                raw_response=response,
                model=model,
                success=True
            )
            
        except Exception as e:
            raise Exception(f"Error processing with File API: {str(e)}")
    
    def list_models(self) -> List[str]:
        """List available Gemini models.
        
        Returns:
            List of model names
        """
        try:
            models = self.client.models.list()
            model_names = [model.name for model in models]
            logger.info(f"Found {len(model_names)} available models")
            return model_names
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return []
    
    def get_model_info(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a model.
        
        Args:
            model_name: Name of the model (uses default if not provided)
            
        Returns:
            Dictionary containing model information
        """
        try:
            model_name = model_name or self.model
            model_info = self.client.models.get(model=model_name)
            
            info = {
                "name": model_info.name,
                "display_name": getattr(model_info, 'display_name', 'N/A'),
                "description": getattr(model_info, 'description', 'N/A'),
                "input_token_limit": getattr(model_info, 'input_token_limit', 'N/A'),
                "output_token_limit": getattr(model_info, 'output_token_limit', 'N/A'),
                "supported_generation_methods": getattr(model_info, 'supported_generation_methods', [])
            }
            
            logger.info(f"Retrieved info for model: {model_name}")
            return info
            
        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            return {}


# Convenience function to create a client instance
def create_gemini_client(
    api_key: Optional[str] = None,
    model: Optional[str] = None
) -> GeminiClient:
    """Create a Gemini client instance.
    
    Args:
        api_key: Optional API key (reads from env if not provided)
        model: Optional model name (uses default if not provided)
        
    Returns:
        Configured GeminiClient instance
        
    Example:
        >>> from core.gemini_client import create_gemini_client
        >>> client = create_gemini_client()
        >>> response = client.generate_text("Hello, Gemini!")
    """
    return GeminiClient(api_key=api_key, model=model)
