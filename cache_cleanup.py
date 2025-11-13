#!/usr/bin/env python3
"""
Cache Cleanup Script

Removes Python cache files and directories to clean up the project:
- .pyc files (compiled Python files)
- __pycache__ directories (Python cache folders)
- .pyo files (optimized Python files)

Excludes virtual environment directories (venv, .venv, env, .env, virtualenv, .virtualenv)

Usage:
    python cache_cleanup.py              # Clean current directory
    python cache_cleanup.py --dry-run    # Show what would be deleted (no actual deletion)
    python cache_cleanup.py --verbose    # Show detailed output
"""

import os
import shutil
import argparse
from pathlib import Path


def find_cache_files_and_dirs(root_path: Path, verbose: bool = False):
    """
    Find all Python cache files and directories recursively
    
    Args:
        root_path: Root directory to search from
        verbose: Print detailed information
        
    Returns:
        tuple: (cache_files, cache_dirs) - lists of files and directories to delete
    """
    cache_files = []
    cache_dirs = []
    
    # Directories to exclude from cleanup
    excluded_dirs = {'venv', '.venv', 'env', '.env', 'virtualenv', '.virtualenv'}
    
    if verbose:
        print(f"🔍 Scanning directory: {root_path}")
        print(f"🚫 Excluding directories: {', '.join(excluded_dirs)}")
    
    for root, dirs, files in os.walk(root_path):
        root_path_obj = Path(root)
        
        # Skip if we're inside an excluded directory
        path_parts = root_path_obj.parts
        if any(part in excluded_dirs for part in path_parts):
            if verbose:
                print(f"⏭️  Skipping excluded directory: {root_path_obj}")
            continue
        
        # Remove excluded directories from dirs to prevent os.walk from entering them
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        # Find __pycache__ directories
        if '__pycache__' in dirs:
            cache_dir = root_path_obj / '__pycache__'
            cache_dirs.append(cache_dir)
            if verbose:
                print(f"📁 Found cache directory: {cache_dir}")
        
        # Find .pyc and .pyo files
        for file in files:
            if file.endswith(('.pyc', '.pyo')):
                cache_file = root_path_obj / file
                cache_files.append(cache_file)
                if verbose:
                    print(f"📄 Found cache file: {cache_file}")
    
    return cache_files, cache_dirs


def clean_cache(root_path: Path = None, dry_run: bool = False, verbose: bool = False):
    """
    Clean Python cache files and directories
    
    Args:
        root_path: Root directory to clean (defaults to current directory)
        dry_run: If True, only show what would be deleted without actually deleting
        verbose: Show detailed output
    """
    if root_path is None:
        root_path = Path.cwd()
    
    if not root_path.exists():
        print(f"❌ Error: Directory {root_path} does not exist")
        return
    
    print(f"🧹 Python Cache Cleanup")
    print(f"📂 Target directory: {root_path}")
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be deleted")
    print("-" * 50)
    
    # Find all cache files and directories
    cache_files, cache_dirs = find_cache_files_and_dirs(root_path, verbose)
    
    total_files = len(cache_files)
    total_dirs = len(cache_dirs)
    total_items = total_files + total_dirs
    
    if total_items == 0:
        print("✅ No Python cache files or directories found!")
        return
    
    print(f"\n📊 Found {total_files} cache files and {total_dirs} cache directories")
    
    if not dry_run:
        # Ask for confirmation unless in non-interactive mode
        if os.isatty(0):  # Check if running in interactive terminal
            response = input(f"\n❓ Delete {total_items} items? (y/N): ").lower().strip()
            if response not in ['y', 'yes']:
                print("❌ Cleanup cancelled")
                return
    
    deleted_files = 0
    deleted_dirs = 0
    errors = []
    
    # Delete cache files
    for cache_file in cache_files:
        try:
            if not dry_run:
                cache_file.unlink()
                deleted_files += 1
            if verbose or dry_run:
                action = "Would delete" if dry_run else "Deleted"
                print(f"🗑️  {action} file: {cache_file}")
        except Exception as e:
            error_msg = f"Failed to delete file {cache_file}: {e}"
            errors.append(error_msg)
            if verbose:
                print(f"❌ {error_msg}")
    
    # Delete cache directories
    for cache_dir in cache_dirs:
        try:
            if not dry_run:
                shutil.rmtree(cache_dir)
                deleted_dirs += 1
            if verbose or dry_run:
                action = "Would delete" if dry_run else "Deleted"
                print(f"🗑️  {action} directory: {cache_dir}")
        except Exception as e:
            error_msg = f"Failed to delete directory {cache_dir}: {e}"
            errors.append(error_msg)
            if verbose:
                print(f"❌ {error_msg}")
    
    # Summary
    print("\n" + "=" * 50)
    if dry_run:
        print(f"📋 DRY RUN SUMMARY:")
        print(f"   Would delete {total_files} cache files")
        print(f"   Would delete {total_dirs} cache directories")
        print(f"   Total items: {total_items}")
    else:
        print(f"✅ CLEANUP COMPLETE:")
        print(f"   Deleted {deleted_files}/{total_files} cache files")
        print(f"   Deleted {deleted_dirs}/{total_dirs} cache directories")
        print(f"   Total deleted: {deleted_files + deleted_dirs}/{total_items}")
    
    if errors:
        print(f"\n⚠️  {len(errors)} errors occurred:")
        for error in errors:
            print(f"   {error}")
    
    if not dry_run and deleted_files + deleted_dirs > 0:
        print("\n🎉 Python cache cleanup completed successfully!")


def get_directory_size(path: Path):
    """Calculate total size of directory in bytes"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
    except Exception:
        pass
    return total_size


def format_size(size_bytes: int) -> str:
    """Format size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def show_size_info(root_path: Path):
    """Show size information for cache directories"""
    cache_files, cache_dirs = find_cache_files_and_dirs(root_path)
    
    total_size = 0
    
    # Calculate size of cache files
    for cache_file in cache_files:
        try:
            total_size += cache_file.stat().st_size
        except Exception:
            pass
    
    # Calculate size of cache directories
    for cache_dir in cache_dirs:
        total_size += get_directory_size(cache_dir)
    
    if total_size > 0:
        print(f"💾 Total cache size: {format_size(total_size)}")
    
    return total_size


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(
        description="Clean Python cache files and directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cache_cleanup.py                    # Clean current directory
  python cache_cleanup.py --dry-run          # Show what would be deleted
  python cache_cleanup.py --verbose          # Show detailed output
  python cache_cleanup.py --path /some/dir   # Clean specific directory
  python cache_cleanup.py --size             # Show cache size information
        """
    )
    
    parser.add_argument(
        '--path', '-p',
        type=str,
        help='Path to clean (default: current directory)'
    )
    
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be deleted without actually deleting'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    
    parser.add_argument(
        '--size', '-s',
        action='store_true',
        help='Show cache size information'
    )
    
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt (non-interactive mode)'
    )
    
    args = parser.parse_args()
    
    # Determine target path
    target_path = Path(args.path) if args.path else Path.cwd()
    
    try:
        # Show size information if requested
        if args.size:
            print(f"📊 Cache Size Analysis for: {target_path}")
            print("-" * 50)
            total_size = show_size_info(target_path)
            if total_size == 0:
                print("✅ No cache files found")
            return
        
        # Handle non-interactive mode
        if args.yes:
            # Temporarily redirect stdin to simulate non-interactive environment
            import sys
            sys.stdin = open(os.devnull)
        
        # Perform cleanup
        clean_cache(
            root_path=target_path,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
        
    except KeyboardInterrupt:
        print("\n❌ Cleanup cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()