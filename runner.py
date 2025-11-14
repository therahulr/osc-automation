"""
OSC Automation Runner

Interactive runner for OSC automation scripts with custom data handling.
Provides user-friendly prompts for custom data file creation and management.

Features:
- Interactive custom data file creation
- Multiple script execution options
- Error handling and logging
- User-friendly prompts and confirmations

Usage:
    python runner.py create_credit_card_merchant
    python runner.py create_credit_card_merchant --custom-data
    python runner.py create_credit_card_merchant --custom-data existing_file.txt
    python runner.py --list-scripts
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import time

# Add project paths
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))

from utils.custom_data import (
    CustomDataManager, 
    load_and_apply_custom_data,
    create_custom_data_skeleton,
    create_custom_data_example
)
from core.logger import setup_logging
from data.osc.osc_data import get_all_data

logger = logging.getLogger(__name__)


class OSCRunner:
    """
    Main runner class for OSC automation scripts
    
    Handles script execution, custom data management, and user interactions
    """
    
    def __init__(self):
        self.available_scripts = {
            "create_credit_card_merchant": {
                "script": "scripts.osc.create_credit_card_merchant",
                "function": "run_credit_card_merchant_workflow",
                "description": "Create a new credit card merchant application"
            }
            # Add more scripts here as they are developed
        }
        
        self.custom_data_manager = CustomDataManager()
    
    def run_script(self, script_name: str, custom_data_file: Optional[str] = None, 
                   **kwargs) -> Dict:
        """
        Run a specified automation script
        
        Args:
            script_name: Name of script to run
            custom_data_file: Optional path to custom data file
            **kwargs: Additional arguments to pass to script
            
        Returns:
            Dict containing execution results
        """
        try:
            logger.info(f"Running script: {script_name}")
            
            if script_name not in self.available_scripts:
                raise ValueError(f"Unknown script: {script_name}")
            
            script_info = self.available_scripts[script_name]
            
            # Import and run the script
            module_name = script_info["script"]
            function_name = script_info["function"]
            
            # Dynamic import
            module = __import__(module_name, fromlist=[function_name])
            script_function = getattr(module, function_name)
            
            # Run with custom data if provided
            if custom_data_file:
                results = script_function(custom_data_file=custom_data_file, **kwargs)
            else:
                results = script_function(**kwargs)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to run script {script_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "script_name": script_name
            }
    
    def handle_custom_data_flow(self) -> Optional[str]:
        """
        Handle the interactive custom data flow
        
        Returns:
            Optional[str]: Path to custom data file if created/selected, None otherwise
        """
        try:
            print("\\n🔧 Custom Data Override")
            print("You chose to use custom data to override default values.")
            
            # Initial confirmation
            confirm = self._get_user_confirmation(
                "Do you want to proceed with custom data? (Y/n)", 
                default=True
            )
            
            if not confirm:
                print("Proceeding with default data values.")
                return None
            
            # Ask if user has existing file or wants to create new one
            print("\\nCustom data options:")
            print("1. I have an existing custom data file")
            print("2. Create a new custom data file")
            print("3. View example custom data file")
            
            while True:
                choice = input("\\nSelect option (1/2/3): ").strip()
                
                if choice == "1":
                    return self._handle_existing_file()
                elif choice == "2":
                    return self._handle_create_new_file()
                elif choice == "3":
                    self._show_example_file()
                    continue
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
        
        except KeyboardInterrupt:
            print("\\n\\nOperation cancelled by user.")
            return None
        except Exception as e:
            logger.error(f"Error in custom data flow: {e}")
            print(f"Error: {e}")
            return None
    
    def _handle_existing_file(self) -> Optional[str]:
        """Handle existing custom data file selection"""
        print("\\n📁 Existing Custom Data File")
        print("Please provide the path to your custom data file.")
        print("Supported formats: .txt, .json, .yaml, .py")
        print("You can:")
        print("- Type the full path")
        print("- Drag and drop the file (then press Enter)")
        print("- Copy and paste the path")
        
        while True:
            file_path = input("\\nFile path: ").strip()
            
            if not file_path:
                print("Please provide a file path.")
                continue
            
            # Clean up the path (remove quotes if present)
            file_path = file_path.strip('\'"')
            
            # Check if file exists
            path_obj = Path(file_path)
            if not path_obj.exists():
                print(f"❌ File not found: {file_path}")
                
                retry = self._get_user_confirmation("Try another file? (Y/n)", default=True)
                if not retry:
                    return None
                continue
            
            # Validate file format
            extension = path_obj.suffix.lower().lstrip('.')
            if extension not in self.custom_data_manager.supported_formats:
                print(f"❌ Unsupported file format: .{extension}")
                print(f"Supported formats: {', '.join(self.custom_data_manager.supported_formats)}")
                continue
            
            # Try to load and validate the file
            try:
                custom_data = self.custom_data_manager.load_custom_data(file_path)
                is_valid, errors = self.custom_data_manager.validate_custom_data(custom_data)
                
                if not is_valid:
                    print(f"⚠️  File has validation errors:")
                    for error in errors:
                        print(f"   - {error}")
                    
                    use_anyway = self._get_user_confirmation(
                        "Use file anyway? (some values may be ignored) (y/N)", 
                        default=False
                    )
                    if not use_anyway:
                        continue
                
                print(f"✅ Custom data file loaded: {file_path}")
                print(f"   Found {len(custom_data)} custom values")
                return str(path_obj.absolute())
                
            except Exception as e:
                print(f"❌ Error loading file: {e}")
                continue
    
    def _handle_create_new_file(self) -> Optional[str]:
        """Handle creation of new custom data file"""
        print("\\n📝 Create New Custom Data File")
        
        # Choose file type
        print("Select file format:")
        print("1. TXT (simple key=value format) - Recommended for beginners")
        print("2. JSON (structured format)")
        print("3. Generate skeleton file and edit manually")
        
        while True:
            format_choice = input("\\nSelect format (1/2/3): ").strip()
            
            if format_choice == "1":
                return self._create_txt_file()
            elif format_choice == "2":
                return self._create_json_file()
            elif format_choice == "3":
                return self._create_skeleton_file()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    
    def _create_txt_file(self) -> Optional[str]:
        """Create a new TXT format custom data file"""
        print("\\n📄 Creating TXT Custom Data File")
        
        # Get filename
        default_name = f"custom_data_{int(time.time())}.txt"
        filename = input(f"\\nFilename ({default_name}): ").strip() or default_name
        
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        output_path = self.custom_data_manager.base_data_dir / filename
        
        # Show common fields for customization
        print("\\nCommon fields you might want to customize:")
        print("(Leave empty to skip, or enter new value)")
        
        common_fields = {
            "SALES_REPRESENTATIVE.name": "DEMONET1",
            "MERCHANT_INFO.legal_business_name": "Test Merchant Solutions LLC",
            "MERCHANT_INFO.dba_name": "Test Merchant Store",
            "PRINCIPAL_INFO.first_name": "John",
            "PRINCIPAL_INFO.last_name": "Doe",
            "PRINCIPAL_INFO.email": "john.doe@testmerchant.com",
            "BUSINESS_ADDRESS.street_address": "123 Business Ave",
            "BUSINESS_ADDRESS.city": "Test City",
            "BUSINESS_ADDRESS.state": "CA"
        }
        
        custom_values = {}
        for field, default_value in common_fields.items():
            print(f"\\n{field}")
            print(f"  Default: {default_value}")
            new_value = input("  Custom value: ").strip()
            
            if new_value:
                custom_values[field] = new_value
        
        # Generate file content
        content_lines = [
            "# OSC Custom Data Override File",
            f"# Created: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "#",
            "# Format: key=value",
            "# You can add more fields as needed",
            ""
        ]
        
        for field, value in custom_values.items():
            content_lines.append(f"{field}={value}")
        
        if not custom_values:
            content_lines.extend([
                "# No custom values specified",
                "# Add your custom values below:",
                "# SALES_REPRESENTATIVE.name=DEMONET2",
                "# MERCHANT_INFO.legal_business_name=My Business Name"
            ])
        
        # Write file
        try:
            output_path.write_text('\\n'.join(content_lines), encoding='utf-8')
            print(f"\\n✅ Custom data file created: {output_path}")
            
            if custom_values:
                print(f"   Contains {len(custom_values)} custom values")
            else:
                print("   File created as template - add your values and re-run")
                
                edit_now = self._get_user_confirmation(
                    "Open file for editing now? (Y/n)", 
                    default=True
                )
                if edit_now:
                    self._open_file_for_editing(output_path)
            
            return str(output_path.absolute())
            
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            return None
    
    def _create_json_file(self) -> Optional[str]:
        """Create a new JSON format custom data file"""
        print("\\n📄 Creating JSON Custom Data File")
        
        # Get filename
        default_name = f"custom_data_{int(time.time())}.json"
        filename = input(f"\\nFilename ({default_name}): ").strip() or default_name
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        output_path = self.custom_data_manager.base_data_dir / filename
        
        # Create basic structure
        custom_data = {
            "SALES_REPRESENTATIVE.name": "DEMONET1",
            "MERCHANT_INFO.legal_business_name": "Custom Business Name",
            "PRINCIPAL_INFO.first_name": "John",
            "PRINCIPAL_INFO.last_name": "Doe"
        }
        
        try:
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(custom_data, f, indent=2)
            
            print(f"\\n✅ JSON custom data file created: {output_path}")
            print("   Edit the file to customize values")
            
            return str(output_path.absolute())
            
        except Exception as e:
            print(f"❌ Error creating JSON file: {e}")
            return None
    
    def _create_skeleton_file(self) -> Optional[str]:
        """Create skeleton file with all available fields"""
        print("\\n📋 Creating Skeleton File")
        
        try:
            skeleton_path = self.custom_data_manager.generate_skeleton_file()
            print(f"\\n✅ Skeleton file created: {skeleton_path}")
            print("   This file contains ALL available fields for customization")
            print("   Uncomment and modify the lines you want to customize")
            
            self._open_file_for_editing(skeleton_path)
            
            return str(skeleton_path.absolute())
            
        except Exception as e:
            print(f"❌ Error creating skeleton file: {e}")
            return None
    
    def _show_example_file(self):
        """Show example custom data file"""
        print("\\n📖 Example Custom Data File")
        
        try:
            example_path = self.custom_data_manager.generate_example_file()
            
            # Read and display content
            content = example_path.read_text(encoding='utf-8')
            print("\\n" + "="*50)
            print(content)
            print("="*50 + "\\n")
            
            print(f"Example file saved: {example_path}")
            
        except Exception as e:
            print(f"❌ Error showing example: {e}")
    
    def _open_file_for_editing(self, file_path: Path):
        """Attempt to open file in default editor"""
        try:
            import subprocess
            import platform
            
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", str(file_path)])
            elif system == "Windows":
                subprocess.run(["notepad", str(file_path)])
            else:  # Linux
                subprocess.run(["xdg-open", str(file_path)])
                
            print(f"\\n📝 Opening file in default editor...")
            print("   Save the file when you're done editing")
            
            input("\\nPress Enter when you've finished editing the file...")
            
        except Exception as e:
            print(f"\\n⚠️  Could not open file automatically: {e}")
            print(f"Please manually edit: {file_path}")
    
    def _get_user_confirmation(self, prompt: str, default: bool = True) -> bool:
        """Get yes/no confirmation from user"""
        suffix = " [Y/n]" if default else " [y/N]"
        
        while True:
            response = input(prompt + suffix + ": ").strip().lower()
            
            if response == "":
                return default
            elif response in ("y", "yes"):
                return True
            elif response in ("n", "no"):
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    def list_available_scripts(self):
        """Display list of available scripts"""
        print("\\n📋 Available OSC Automation Scripts:")
        print("-" * 50)
        
        for name, info in self.available_scripts.items():
            print(f"\\n• {name}")
            print(f"  {info['description']}")
        
        print("\\nUsage examples:")
        print("  python runner.py create_credit_card_merchant")
        print("  python runner.py create_credit_card_merchant --custom-data")
        print("  python runner.py create_credit_card_merchant --custom-data my_data.txt")


def main():
    """Main entry point for the runner"""
    parser = argparse.ArgumentParser(
        description="OSC Automation Runner - Execute automation scripts with custom data support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python runner.py create_credit_card_merchant
  python runner.py create_credit_card_merchant --custom-data
  python runner.py create_credit_card_merchant --custom-data existing_file.txt
  python runner.py --list-scripts
        """
    )
    
    parser.add_argument(
        "script_name", 
        nargs="?",
        help="Name of the automation script to run"
    )
    
    parser.add_argument(
        "--custom-data", 
        nargs="?", 
        const="interactive",
        help="Use custom data (interactive mode if no file specified)"
    )
    
    parser.add_argument(
        "--list-scripts", 
        action="store_true",
        help="List all available automation scripts"
    )
    
    parser.add_argument(
        "--headless", 
        action="store_true", 
        default=True,
        help="Run browser in headless mode (default)"
    )
    
    parser.add_argument(
        "--headed", 
        action="store_true",
        help="Run browser in headed mode (visible browser)"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level)
    
    # Create runner
    runner = OSCRunner()
    
    try:
        # Handle list scripts
        if args.list_scripts:
            runner.list_available_scripts()
            return 0
        
        # Validate script name
        if not args.script_name:
            print("❌ Error: No script name provided")
            print("\\nUse --list-scripts to see available scripts")
            return 1
        
        if args.script_name not in runner.available_scripts:
            print(f"❌ Error: Unknown script '{args.script_name}'")
            print("\\nUse --list-scripts to see available scripts")
            return 1
        
        # Handle custom data
        custom_data_file = None
        if args.custom_data:
            if args.custom_data == "interactive":
                custom_data_file = runner.handle_custom_data_flow()
            else:
                custom_data_file = args.custom_data
                
                # Validate file exists
                if not Path(custom_data_file).exists():
                    print(f"❌ Error: Custom data file not found: {custom_data_file}")
                    return 1
        
        # Determine headless mode
        headless = args.headless and not args.headed
        
        # Run the script
        print(f"\\n🚀 Running {args.script_name}...")
        if custom_data_file:
            print(f"   Using custom data: {custom_data_file}")
        print(f"   Browser mode: {'headless' if headless else 'headed'}")
        
        results = runner.run_script(
            args.script_name, 
            custom_data_file=custom_data_file,
            headless=headless
        )
        
        # Display results
        if results.get("success"):
            print("\\n✅ Script completed successfully!")
            if "application_form_url" in results:
                print(f"   Application form URL: {results['application_form_url']}")
            if "screenshots" in results and results["screenshots"]:
                print(f"   Screenshots saved: {len(results['screenshots'])}")
        else:
            print("\\n❌ Script failed!")
            print(f"   Error: {results.get('error', 'Unknown error')}")
            if "step_completed" in results:
                print(f"   Failed at step: {results['step_completed']}")
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\\n\\n⚠️  Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Runner error: {e}")
        print(f"\\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())