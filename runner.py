"""
OSC Automation Runner - Interactive CLI

Beautiful, interactive command-line interface for running OSC automation scripts.
Uses Rich library for colorful, interactive terminal UI.

Features:
- Interactive script selection menu
- Real-time progress display
- Colorful output with Rich
- Script execution with live status updates

Usage:
    python runner.py              # Interactive mode
    python runner.py --list       # List available scripts
    python runner.py <script>     # Run specific script directly
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import importlib
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Rich imports for beautiful CLI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.text import Text
    from rich.markdown import Markdown
    from rich.live import Live
    from rich.layout import Layout
    from rich import box
    from rich.style import Style
    from rich.theme import Theme
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Rich library not installed. Install with: pip install rich")
    print("   Falling back to basic mode.\n")

# Custom theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "title": "bold magenta",
    "script": "bold cyan",
    "description": "dim white",
})

console = Console(theme=custom_theme) if RICH_AVAILABLE else None


class ScriptInfo:
    """Information about an automation script"""
    def __init__(self, name: str, module: str, function: str, description: str, tags: List[str] = None):
        self.name = name
        self.module = module
        self.function = function
        self.description = description
        self.tags = tags or []


# Available scripts registry
AVAILABLE_SCRIPTS: Dict[str, ScriptInfo] = {
    "create_credit_card_merchant": ScriptInfo(
        name="Create Credit Card Merchant",
        module="scripts.osc.create_credit_card_merchant",
        function="create_credit_card_merchant",
        description="Create a new credit card merchant application with all required fields",
        tags=["merchant", "credit-card", "application"]
    ),
    "create_credit_ach_merchant": ScriptInfo(
        name="Create Credit Card + ACH Merchant",
        module="scripts.osc.create_credit_ach_merchant",
        function="create_credit_ach_merchant",
        description="Create a merchant application with Credit Card and ACH products",
        tags=["merchant", "credit-card", "ach", "application"]
    ),
    "verify_dashboard": ScriptInfo(
        name="Verify Dashboard",
        module="scripts.osc.verify_dashboard",
        function="verify_dashboard",
        description="Verify OSC dashboard elements and navigation",
        tags=["dashboard", "verification"]
    ),
}


def print_banner():
    """Print the application banner"""
    if not RICH_AVAILABLE:
        print("\n" + "="*60)
        print("  OSC AUTOMATION RUNNER")
        print("="*60 + "\n")
        return
    
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ██████╗ ███████╗ ██████╗                                  ║
║    ██╔═══██╗██╔════╝██╔════╝                                  ║
║    ██║   ██║███████╗██║                                       ║
║    ██║   ██║╚════██║██║                                       ║
║    ╚██████╔╝███████║╚██████╗                                  ║
║     ╚═════╝ ╚══════╝ ╚═════╝                                  ║
║                                                               ║
║         🚀  AUTOMATION RUNNER  🚀                             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def list_scripts():
    """Display available scripts in a beautiful table"""
    if not RICH_AVAILABLE:
        print("\nAvailable Scripts:")
        print("-" * 50)
        for idx, (key, script) in enumerate(AVAILABLE_SCRIPTS.items(), 1):
            print(f"  {idx}. {script.name}")
            print(f"     Command: python runner.py {key}")
            print(f"     {script.description}\n")
        return
    
    table = Table(
        title="📋 Available Automation Scripts",
        box=box.ROUNDED,
        header_style="bold magenta",
        title_style="bold white",
        border_style="cyan"
    )
    
    table.add_column("#", style="dim", width=3, justify="center")
    table.add_column("Script Name", style="cyan bold", width=30)
    table.add_column("Description", style="white", width=50)
    table.add_column("Tags", style="dim green", width=20)
    
    for idx, (key, script) in enumerate(AVAILABLE_SCRIPTS.items(), 1):
        tags = ", ".join(script.tags) if script.tags else "-"
        table.add_row(
            str(idx),
            f"{script.name}\n[dim]{key}[/dim]",
            script.description,
            tags
        )
    
    console.print()
    console.print(table)
    console.print()


def select_script_interactive() -> Optional[str]:
    """Interactive script selection menu"""
    if not RICH_AVAILABLE:
        print("\nSelect a script to run:")
        scripts_list = list(AVAILABLE_SCRIPTS.keys())
        for idx, key in enumerate(scripts_list, 1):
            script = AVAILABLE_SCRIPTS[key]
            print(f"  {idx}. {script.name}")
        
        try:
            choice = input("\nEnter number (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(scripts_list):
                return scripts_list[idx]
        except (ValueError, IndexError):
            print("Invalid selection")
        return None
    
    # Rich interactive menu
    console.print("\n[bold cyan]Select a script to run:[/bold cyan]\n")
    
    scripts_list = list(AVAILABLE_SCRIPTS.keys())
    
    for idx, key in enumerate(scripts_list, 1):
        script = AVAILABLE_SCRIPTS[key]
        console.print(f"  [bold yellow]{idx}[/bold yellow]. [cyan]{script.name}[/cyan]")
        console.print(f"     [dim]{script.description}[/dim]\n")
    
    console.print(f"  [bold yellow]0[/bold yellow]. [red]Exit[/red]\n")
    
    while True:
        choice = Prompt.ask(
            "[bold white]Enter your choice[/bold white]",
            default="1"
        )
        
        if choice == "0" or choice.lower() == "q":
            return None
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(scripts_list):
                return scripts_list[idx]
            else:
                console.print("[red]Invalid selection. Please try again.[/red]")
        except ValueError:
            # Check if user typed script name directly
            if choice in AVAILABLE_SCRIPTS:
                return choice
            console.print("[red]Invalid input. Please enter a number.[/red]")


def confirm_execution(script_key: str) -> bool:
    """Confirm script execution with user"""
    script = AVAILABLE_SCRIPTS[script_key]
    
    if not RICH_AVAILABLE:
        print(f"\n📋 Script: {script.name}")
        print(f"   {script.description}")
        response = input("\nProceed? (Y/n): ").strip().lower()
        return response in ('', 'y', 'yes')
    
    console.print()
    panel = Panel(
        f"[cyan]{script.description}[/cyan]\n\n"
        f"[dim]Module: {script.module}[/dim]\n"
        f"[dim]Function: {script.function}[/dim]",
        title=f"[bold green]📋 {script.name}[/bold green]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(panel)
    
    return Confirm.ask("\n[bold]Proceed with execution?[/bold]", default=True)


def run_script(script_key: str) -> Dict[str, Any]:
    """Execute the selected script"""
    script = AVAILABLE_SCRIPTS[script_key]
    
    if not RICH_AVAILABLE:
        print(f"\n🚀 Running: {script.name}...")
        print("-" * 50)
    else:
        console.print()
        console.print(Panel(
            f"[bold cyan]Executing: {script.name}[/bold cyan]",
            border_style="cyan"
        ))
    
    try:
        # Dynamic import
        module = importlib.import_module(script.module)
        script_function = getattr(module, script.function)
        
        # Execute the script
        start_time = time.time()
        results = script_function()
        elapsed_time = time.time() - start_time
        
        # Add timing info
        if results is None:
            results = {}
        results["elapsed_time"] = elapsed_time
        results["success"] = results.get("success", True)
        
        return results
        
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
        else:
            print(f"\n❌ Error: {str(e)}")
        
        import traceback
        traceback.print_exc()
        
        return {
            "success": False,
            "error": str(e)
        }


def display_results(results: Dict[str, Any], script_key: str):
    """Display execution results"""
    script = AVAILABLE_SCRIPTS[script_key]
    
    if not RICH_AVAILABLE:
        print("\n" + "="*50)
        if results.get("success"):
            print("✅ SUCCESS")
        else:
            print("❌ FAILED")
        
        if "app_info_id" in results:
            print(f"   AppInfoID: {results['app_info_id']}")
        if "elapsed_time" in results:
            print(f"   Time: {results['elapsed_time']:.2f}s")
        if "error" in results:
            print(f"   Error: {results['error']}")
        print("="*50)
        return
    
    console.print()
    
    if results.get("success"):
        # Success panel
        success_content = "[bold green]✅ Script completed successfully![/bold green]\n\n"
        
        if "app_info_id" in results and results["app_info_id"]:
            success_content += f"[cyan]📋 AppInfoID:[/cyan] [bold white]{results['app_info_id']}[/bold white]\n"
        
        if "elapsed_time" in results:
            success_content += f"[cyan]⏱️  Duration:[/cyan] [white]{results['elapsed_time']:.2f} seconds[/white]\n"
        
        if "summary" in results:
            summary = results["summary"]
            success_content += f"\n[cyan]📊 Summary:[/cyan]\n"
            success_content += f"   Total Fields: {summary.get('total_fields', 'N/A')}\n"
            success_content += f"   Success Rate: {summary.get('success_rate', 'N/A')}\n"
        
        console.print(Panel(
            success_content,
            title=f"[bold green]🎉 {script.name} - Complete[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
    else:
        # Error panel
        error_content = "[bold red]❌ Script execution failed[/bold red]\n\n"
        
        if "error" in results:
            error_content += f"[red]Error:[/red] {results['error']}\n"
        
        if "elapsed_time" in results:
            error_content += f"\n[dim]Duration: {results['elapsed_time']:.2f} seconds[/dim]"
        
        console.print(Panel(
            error_content,
            title=f"[bold red]💥 {script.name} - Failed[/bold red]",
            border_style="red",
            padding=(1, 2)
        ))


def interactive_mode():
    """Run in interactive mode with menu"""
    print_banner()
    
    while True:
        list_scripts()
        
        script_key = select_script_interactive()
        
        if script_key is None:
            if RICH_AVAILABLE:
                console.print("\n[yellow]👋 Goodbye![/yellow]\n")
            else:
                print("\n👋 Goodbye!\n")
            break
        
        if confirm_execution(script_key):
            results = run_script(script_key)
            display_results(results, script_key)
        
        if RICH_AVAILABLE:
            console.print()
            if not Confirm.ask("[bold]Run another script?[/bold]", default=False):
                console.print("\n[yellow]👋 Goodbye![/yellow]\n")
                break
        else:
            response = input("\nRun another script? (y/N): ").strip().lower()
            if response not in ('y', 'yes'):
                print("\n👋 Goodbye!\n")
                break


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="OSC Automation Runner - Interactive CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python runner.py                          # Interactive mode
  python runner.py --list                   # List available scripts
  python runner.py create_credit_card_merchant   # Run specific script

Available Scripts:
  - create_credit_card_merchant    Create Credit Card merchant
  - create_credit_ach_merchant     Create Credit Card + ACH merchant
  - verify_dashboard               Verify OSC dashboard
        """
    )
    
    parser.add_argument(
        "script",
        nargs="?",
        help="Script name to run directly (skip interactive menu)"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available scripts"
    )
    
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Skip confirmation prompts"
    )
    
    args = parser.parse_args()
    
    # List scripts mode
    if args.list:
        print_banner()
        list_scripts()
        
        if RICH_AVAILABLE:
            console.print("[dim]Usage: python runner.py <script_name>[/dim]\n")
        else:
            print("Usage: python runner.py <script_name>\n")
        return 0
    
    # Direct script execution
    if args.script:
        if args.script not in AVAILABLE_SCRIPTS:
            if RICH_AVAILABLE:
                console.print(f"[bold red]❌ Unknown script:[/bold red] {args.script}")
                console.print("\n[yellow]Available scripts:[/yellow]")
                for key in AVAILABLE_SCRIPTS:
                    console.print(f"  • {key}")
            else:
                print(f"❌ Unknown script: {args.script}")
                print("\nAvailable scripts:")
                for key in AVAILABLE_SCRIPTS:
                    print(f"  • {key}")
            return 1
        
        print_banner()
        
        if not args.yes and not confirm_execution(args.script):
            if RICH_AVAILABLE:
                console.print("[yellow]Cancelled.[/yellow]")
            else:
                print("Cancelled.")
            return 0
        
        results = run_script(args.script)
        display_results(results, args.script)
        
        return 0 if results.get("success") else 1
    
    # Interactive mode (default)
    interactive_mode()
    return 0


if __name__ == "__main__":
    sys.exit(main())
