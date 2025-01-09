#!/usr/bin/env python3

import argparse
import os
import re
import logging
from pathlib import Path
from datetime import datetime
import subprocess
from typing import Tuple

"""
Jekyll Include File Migration Tool

This script facilitates the migration of Jekyll include files from one directory to another,
including updating all references to these files throughout the Jekyll site.

Features:
- Move include files between directories
- Rename specific files during migration
- Update all references in .html, .md, and .markdown files
- Support for both {% include %} and {%- include -%} syntax
- Dry run capability to preview changes
- Comprehensive logging
"""

def setup_logging(log_file=None, debug=False):
    """
    Configure logging to both file and console.
    """
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Create logger
    logger = logging.getLogger('include_migrator')
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.addHandler(console_handler)
    
    # File handler if log file specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
        logger.addHandler(file_handler)
    
    return logger

def update_include_references(file_path, old_dir, new_dir, old_name=None, new_name=None, dry_run=False, logger=None):
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Updated patterns to handle multi-line includes with arguments
    patterns = [
        r'{%\s*include\s+([^\s%}]+)(?:\s+[^%}]+)?%}',  # Standard include with optional args
        r'{%-\s*include\s+([^\s%}]+)(?:\s+[^%}]+)?-%}',  # Whitespace trimmed include with optional args
        r'{%-\s*include\s+([^\s%}]+)(?:\s+[^%}]+)?%}',  # Mixed trimming with optional args
        r'{%\s*include\s+([^\s%}]+)(?:\s+[^%}]+)?-%}'   # Mixed trimming with optional args
    ]
    
    new_content = content
    changes_made = False
    found_includes = set()
    
    for pattern in patterns:
        # Use re.DOTALL to make . match newlines as well
        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            path = match.group(1)
            if old_name and new_name:
                if old_dir == ".":
                    if path == old_name:
                        found_includes.add(f"{path} -> {new_dir}/{new_name}")
                        new_content = new_content.replace(match.group(1), f"{new_dir}/{new_name}")
                        changes_made = True
                elif path.startswith(f"{old_dir}/"):
                    filename = path.split('/')[-1]
                    if filename == old_name:
                        found_includes.add(f"{path} -> {new_dir}/{new_name}")
                        new_content = new_content.replace(path, f"{new_dir}/{new_name}")
                        changes_made = True
    
    if changes_made:
        if dry_run:
            logger.info(f"Would update references in: {file_path}")
            for include in sorted(found_includes):
                logger.info(f"  - Would change include: {include}")
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            logger.info(f"Updated references in: {file_path}")
            for include in sorted(found_includes):
                logger.info(f"  - Changed include: {include}")

def move_include_files(jekyll_root, old_dir, new_dir, old_name=None, new_name=None, dry_run=False, logger=None, includes_dir='_includes'):
    """
    Move files from old include directory to new one.
    
    Args:
        jekyll_root (Path): Root directory of Jekyll site
        old_dir (str): Current include directory name
        new_dir (str): New include directory name
        old_name (str, optional): Original filename to change
        new_name (str, optional): New filename
        dry_run (bool): If True, only show what would be changed
        logger (logging.Logger): Logger instance for output
        includes_dir (str): Name of the includes directory (default: _includes)
    """
    old_include_path = Path(jekyll_root) / includes_dir / old_dir
    new_include_path = Path(jekyll_root) / includes_dir / new_dir
    
    if not old_include_path.exists():
        logger.error(f"Source directory does not exist: {old_include_path}")
        return
    
    if not dry_run:
        new_include_path.mkdir(parents=True, exist_ok=True)
    
    # If we're moving/renaming a specific file
    if old_name and new_name:
        source_file = old_include_path / old_name
        target_file = new_include_path / new_name
        
        if not source_file.exists():
            logger.error(f"Source file does not exist: {source_file}")
            return
            
        if dry_run:
            logger.info(f"Would move: {source_file} -> {target_file}")
        else:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            source_file.rename(target_file)
            logger.info(f"Moved: {source_file} -> {target_file}")
    else:
        # Moving all files from one directory to another
        for file_path in old_include_path.glob('*'):
            new_file_path = new_include_path / file_path.name
            
            if dry_run:
                logger.info(f"Would move: {file_path} -> {new_file_path}")
            else:
                file_path.rename(new_file_path)
                logger.info(f"Moved: {file_path} -> {new_file_path}")
    
    # Only remove the old directory if we moved all files and it's empty
    if not dry_run and not old_name and not any(old_include_path.iterdir()):
        old_include_path.rmdir()
        logger.info(f"Removed empty directory: {old_include_path}")

def run_git_command(command: list[str], logger: logging.Logger) -> Tuple[bool, str]:
    """
    Run a git command and return success status and output.
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {' '.join(command)}")
        logger.error(f"Error output: {e.stderr}")
        return False, e.stderr

def ensure_clean_git_state(jekyll_root: Path, logger: logging.Logger) -> bool:
    """
    Ensure git working directory is clean and up to date.
    """
    # Check if we're in a git repository
    if not (jekyll_root / '.git').exists():
        logger.error("Not a git repository")
        return False

    # Add debug logging for current directory
    logger.debug(f"Checking git status in: {jekyll_root.absolute()}")

    # Check for uncommitted changes with more detailed logging
    success, status_output = run_git_command(['git', '-C', str(jekyll_root), 'status', '--porcelain'], logger)
    if not success:
        return False
    
    logger.debug(f"Git status output: '{status_output}'")
    
    if status_output.strip():
        logger.error(f"Working directory not clean. Status output: {status_output}")
        return False

    # Perform git pull
    logger.info("Pulling latest changes...")
    success, pull_output = run_git_command(['git', '-C', str(jekyll_root), 'pull'], logger)
    if not success:
        return False

    logger.info("Git working directory is clean and up to date")
    return True

def commit_and_push_changes(jekyll_root: Path, old_dir: str, new_dir: str, 
                          old_name: str = None, new_name: str = None, 
                          logger: logging.Logger = None) -> bool:
    """
    Commit changes and push to remote.
    """
    # Construct commit message
    if old_name and new_name:
        message = f"""Migrate Jekyll include file

Move and update references:
- From: {old_dir}/{old_name}
- To: {new_dir}/{new_name}

Automated change via migrate_includes.py"""
    else:
        message = f"""Migrate Jekyll include files

Move all includes and update references:
- From: {old_dir}/
- To: {new_dir}/

Automated change via migrate_includes.py"""

    # Stage changes
    success, _ = run_git_command(['git', 'add', '.'], logger)
    if not success:
        return False

    # Commit changes
    success, _ = run_git_command(['git', 'commit', '-m', message], logger)
    if not success:
        return False

    # Push changes
    logger.info("Pushing changes to remote...")
    success, _ = run_git_command(['git', 'push'], logger)
    if not success:
        return False

    logger.info("Successfully committed and pushed changes")
    return True

def main():
    parser = argparse.ArgumentParser(
        description='''
Migrate Jekyll include files and update references throughout the site.

This tool helps you:
- Move include files between directories
- Rename specific files during migration
- Update all references in .html, .md, and .markdown files
- Support both {% include %} and {%- include -%} syntax
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('old_dir', 
        help='Current include directory name (e.g., "components")')
    parser.add_argument('new_dir', 
        help='New include directory name (e.g., "shared/components")')
    parser.add_argument('--root', 
        default='.', 
        help='Jekyll site root directory (default: current directory)')
    parser.add_argument('--old-name', 
        help='Original filename to change (e.g., "header.html")')
    parser.add_argument('--new-name', 
        help='New filename (required if --old-name is specified)')
    parser.add_argument('--dry-run', 
        action='store_true', 
        help='Show what would be done without making changes')
    parser.add_argument('--log-file', 
        help='Specify a log file to record all operations')
    parser.add_argument('--includes-dir',
        default='_includes',
        help='Name of the includes directory (default: _includes)')
    parser.add_argument('--debug', 
        action='store_true', 
        help='Enable debug logging')
    
    args = parser.parse_args()
    
    if bool(args.old_name) != bool(args.new_name):
        parser.error("--old-name and --new-name must be specified together")
    
    # Setup logging with debug flag
    logger = setup_logging(args.log_file, debug=args.debug)
    
    # Log the start of the operation with all parameters
    logger.info("Starting include migration with parameters:")
    logger.info(f"  Old directory: {args.old_dir}")
    logger.info(f"  New directory: {args.new_dir}")
    logger.info(f"  Root directory: {args.root}")
    logger.info(f"  Old filename: {args.old_name or 'Not specified'}")
    logger.info(f"  New filename: {args.new_name or 'Not specified'}")
    logger.info(f"  Dry run: {args.dry_run}")
    
    jekyll_root = Path(args.root)
    includes_dir = args.includes_dir
    
    if not args.dry_run:
        # Ensure clean git state before proceeding
        if not ensure_clean_git_state(jekyll_root, logger):
            logger.error("Aborting due to git status issues")
            return

    # Move the include files
    move_include_files(jekyll_root, args.old_dir, args.new_dir, 
                      args.old_name, args.new_name, args.dry_run, 
                      logger, includes_dir=args.includes_dir)
    
    # Directories to exclude from search
    excluded_dirs = {'_site', 'node_modules', '.git', '.jekyll-cache', 'vendor'}
    
    logger.info("Scanning for files to update...")
    
    # Debug: Print current working directory
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Jekyll root directory: {jekyll_root.absolute()}")
    
    # Recursive search for all relevant files
    files_found = 0
    files_with_includes = 0
    print(f"\nSearching for files containing includes...")  # Direct debug output
    
    for file_type in ['.html', '.md', '.markdown']:
        for file_path in jekyll_root.rglob(f'*{file_type}'):
            try:
                rel_path = file_path.relative_to(jekyll_root)
                
                if any(excluded in str(rel_path.parts) for excluded in excluded_dirs):
                    continue
                
                files_found += 1
                
                # Quick check for includes
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '{% include' in content:
                        files_with_includes += 1
                
                update_include_references(file_path, args.old_dir, args.new_dir,
                                       args.old_name, args.new_name, args.dry_run, logger)
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")  # Direct debug output
    
    print(f"\nSummary:")  # Direct debug output
    print(f"Total files checked: {files_found}")
    print(f"Files containing includes: {files_with_includes}")
    
    if not args.dry_run:
        # Commit and push changes
        if not commit_and_push_changes(jekyll_root, args.old_dir, args.new_dir, 
                                     args.old_name, args.new_name, logger):
            logger.error("Failed to commit and push changes")
            return

    logger.info("Migration completed successfully")

if __name__ == '__main__':
    main() 