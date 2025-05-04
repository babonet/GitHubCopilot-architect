#!/usr/bin/env python3
"""
utils/tools/file_retriever.py

This module provides functionality for retrieving file contents from a VSCode workspace.
It respects exclusion patterns from config/exclusions.py and formats the output
with file paths and contents in a structured format for AI analysis with GitHub Copilot.

This module is used by the analysis phases to retrieve and process file contents
for deep code analysis using Azure OpenAI integration.
"""

# ====================================================
# Importing Necessary Libraries
# This section imports all the external libraries needed for this script to work.
# Each import statement brings in code from another file or module, making
# those functions and tools available for use here.
# ====================================================

import os
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Generator
import fnmatch
import logging
import json
from config.exclusions import EXCLUDED_DIRS, EXCLUDED_FILES, EXCLUDED_EXTENSIONS

# ====================================================
# Initial Setup
# This part sets up a logger to record important events and messages,
# and defines a list of encodings to handle different file types.
# ====================================================

# Initialize logger
logger = logging.getLogger("github_copilot_architect")

# Define file encoding to try in order of preference
ENCODINGS = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']


# ====================================================
# Function: should_exclude
# This function checks if a given file or directory should be excluded
# based on predefined rules (like excluding certain directory names or file patterns).
# ====================================================

def should_exclude(path: Path, exclude_dirs: Set[str], exclude_patterns: Set[str]) -> bool:
    """
    Determine if a file or directory should be excluded based on exclusion patterns.
    
    Args:
        path: The path to check
        exclude_dirs: Set of directory names to exclude
        exclude_patterns: Set of file patterns to exclude
        
    Returns:
        bool: True if the path should be excluded, False otherwise
    """
    # Check if any part of the path is in excluded dirs
    for part in path.parts:
        if part in exclude_dirs:
            return True
    
    # Check filename against excluded patterns
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path.name, pattern):
            return True
    
    return False


# ====================================================
# Function: read_file_with_fallback
# This function tries to read a file using different encodings.
# If it fails with one encoding, it tries the next until it can read the file.
# ====================================================

def read_file_with_fallback(file_path: Path) -> Tuple[str, str]:
    """
    Read file content with encoding fallback.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Tuple[str, str]: Tuple of (file_content, encoding_used)
    """
    for encoding in ENCODINGS:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content, encoding
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, read as binary and decode with replacement
    with open(file_path, 'rb') as f:
        content = f.read().decode('utf-8', errors='replace')
    return content, 'utf-8 (with replacement)'


# ====================================================
# Function: format_file_content
# This function takes the content of a file and adds the file path
# to the beginning and end, making it easy to identify where the content came from.
# ====================================================

def format_file_content(file_path: Path, content: str) -> str:
    """
    Format file content with file path in the specified format for GitHub Copilot analysis.
    
    Args:
        file_path: Path to the file
        content: File content
        
    Returns:
        str: Formatted file content with path
    """
    relative_path = file_path.as_posix()
    language = detect_language(file_path)
    return f"<file path=\"{relative_path}\" language=\"{language}\">\n{content}\n</file>"


def detect_language(file_path: Path) -> str:
    """
    Detect the programming language based on file extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: Language name or 'text' if unknown
    """
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'jsx',
        '.tsx': 'tsx',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.md': 'markdown',
        '.c': 'c',
        '.cpp': 'cpp',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.cs': 'csharp',
        '.sh': 'shell',
        '.yml': 'yaml', 
        '.yaml': 'yaml',
        '.xml': 'xml',
        '.sql': 'sql',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.dart': 'dart',
        '.vue': 'vue',
        '.scss': 'scss',
        '.less': 'less',
        '.tf': 'terraform',
        '.ps1': 'powershell',
    }
    
    suffix = file_path.suffix.lower()
    return extension_map.get(suffix, 'text')


# ====================================================
# Function: list_files
# This function goes through a directory and finds all files,
# excluding those that match the exclusion rules. It searches
# up to a certain depth (how many folders deep it goes).
# ====================================================

def list_files(
    directory: Path,
    exclude_dirs: Optional[Set[str]] = None,
    exclude_patterns: Optional[Set[str]] = None,
    max_depth: int = 10,
) -> Generator[Path, None, None]:
    """
    List all files in a directory that aren't excluded.
    
    Args:
        directory: Directory to search
        exclude_dirs: Set of directory names to exclude
        exclude_patterns: Set of file patterns to exclude
        max_depth: Maximum depth to search
        
    Yields:
        Path: File paths that match criteria
    """
    if exclude_dirs is None:
        exclude_dirs = EXCLUDED_DIRS
    
    if exclude_patterns is None:
        # Combine excluded files and patterns based on extensions
        exclude_patterns = set()
        # Add excluded files
        for file in EXCLUDED_FILES:
            exclude_patterns.add(file)
        # Add excluded extensions as patterns
        for ext in EXCLUDED_EXTENSIONS:
            exclude_patterns.add(f'*{ext}')
    
    def _list_files_recursive(path: Path, current_depth: int = 0) -> Generator[Path, None, None]:
        if current_depth > max_depth:
            return
        
        try:
            for item in path.iterdir():
                if should_exclude(item, exclude_dirs, exclude_patterns):
                    continue
                
                if item.is_file():
                    yield item
                elif item.is_dir():
                    yield from _list_files_recursive(item, current_depth + 1)
        except PermissionError:
            logger.warning(f"Permission denied: {path}")
    
    yield from _list_files_recursive(directory)


# ====================================================
# Function: get_file_contents
# This function retrieves the contents of all files in a directory,
# while respecting exclusion rules, size limits, and a maximum number of files.
# ====================================================

def get_file_contents(
    directory: Path,
    exclude_dirs: Optional[Set[str]] = None,
    exclude_patterns: Optional[Set[str]] = None,
    max_size_kb: int = 1000,  # Don't process files larger than 1MB by default
    max_files: int = 100,  # Limit the number of files to process
    vscode_config: bool = True  # Whether to include .vscode configuration
) -> Dict[str, str]:
    """
    Get the contents of all files in a directory, excluding those that match exclusion patterns.
    
    Args:
        directory: Directory to search
        exclude_dirs: Set of directory names to exclude
        exclude_patterns: Set of file patterns to exclude
        max_size_kb: Maximum file size in KB to process
        max_files: Maximum number of files to process
        vscode_config: Whether to include .vscode configuration files
        
    Returns:
        Dict[str, str]: Dictionary of {file_path: formatted_content}
    """
    file_contents = {}
    file_count = 0
    
    # Ensure .vscode directory is included if specified
    if vscode_config and exclude_dirs is not None and '.vscode' in exclude_dirs:
        exclude_dirs = exclude_dirs.copy()
        exclude_dirs.remove('.vscode')
    
    for file_path in list_files(directory, exclude_dirs, exclude_patterns):
        if file_count >= max_files:
            logger.warning(f"Reached maximum file limit of {max_files}")
            break
        
        # Check file size
        try:
            file_size_kb = file_path.stat().st_size / 1024
            if file_size_kb > max_size_kb:
                logger.info(f"Skipping large file: {file_path} ({file_size_kb:.2f}KB)")
                continue
            
            # Read file content
            content, encoding = read_file_with_fallback(file_path)
            
            # Format content
            formatted_content = format_file_content(file_path, content)
            
            # Add to dictionary
            relative_path = file_path.relative_to(directory).as_posix()
            file_contents[relative_path] = formatted_content
            file_count += 1
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
    
    return file_contents


# ====================================================
# Function: get_formatted_file_contents
# This function gets all the file contents from a directory
# and combines them into a single string, with each file's content
# clearly marked with its path.
# ====================================================

def get_formatted_file_contents(directory: Path, include_vscode_info: bool = True) -> str:
    """
    Get all file contents formatted with file paths in a single string.
    Includes VSCode workspace information if specified.
    
    Args:
        directory: Directory to search
        include_vscode_info: Whether to include VSCode workspace information
        
    Returns:
        str: All formatted file contents concatenated
    """
    file_contents = get_file_contents(directory, vscode_config=include_vscode_info)
    
    # Add workspace analysis at the beginning if requested
    if include_vscode_info:
        workspace_info = analyze_workspace_structure(directory)
        workspace_json = json.dumps(workspace_info, indent=2)
        workspace_header = f"<workspace_info>\n{workspace_json}\n</workspace_info>"
        return workspace_header + "\n\n" + "\n\n".join(file_contents.values())
    
    return "\n\n".join(file_contents.values())


# ====================================================
# Function: get_filtered_formatted_contents
# This function gets the formatted contents of only specific files
# listed in 'files_to_include'. It's useful for when you only want
# to process certain files and not the entire directory.
# ====================================================

def get_filtered_formatted_contents(directory: Path, files_to_include: List[str], include_vscode_info: bool = True) -> str:
    """
    Get formatted contents for only the specified files.
    Includes VSCode workspace information if specified.
    
    Args:
        directory: Base directory
        files_to_include: List of file paths to include
        include_vscode_info: Whether to include VSCode workspace information
        
    Returns:
        str: Formatted contents of the specified files
    """
    all_contents = get_file_contents(directory, vscode_config=include_vscode_info)
    filtered_contents = []
    
    for file_path in files_to_include:
        if file_path in all_contents:
            filtered_contents.append(all_contents[file_path])
        else:
            # Try to find the file with a fuzzy match
            for path in all_contents:
                if file_path in path or path.endswith(file_path):
                    filtered_contents.append(all_contents[path])
                    break
    
    # Add workspace analysis at the beginning if requested
    if include_vscode_info:
        workspace_info = analyze_workspace_structure(directory)
        workspace_json = json.dumps(workspace_info, indent=2)
        workspace_header = f"<workspace_info>\n{workspace_json}\n</workspace_info>"
        return workspace_header + "\n\n" + "\n\n".join(filtered_contents)
    
    return "\n\n".join(filtered_contents)


# ====================================================
# Additional VSCode-specific functions
# These functions help with parsing and handling VSCode workspace files.
# ====================================================

def get_vscode_settings(directory: Path) -> Dict[str, any]:
    """
    Extract VS Code settings from the .vscode/settings.json file.
    
    Args:
        directory: The workspace directory
        
    Returns:
        Dict[str, any]: VS Code settings or empty dict if not found
    """
    settings_path = directory / '.vscode' / 'settings.json'
    if not settings_path.exists():
        return {}
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading VS Code settings: {e}")
        return {}


def get_vscode_extensions(directory: Path) -> List[str]:
    """
    Extract recommended VS Code extensions from .vscode/extensions.json file.
    
    Args:
        directory: The workspace directory
        
    Returns:
        List[str]: List of recommended extensions or empty list if not found
    """
    extensions_path = directory / '.vscode' / 'extensions.json'
    if not extensions_path.exists():
        return []
    
    try:
        with open(extensions_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('recommendations', [])
    except Exception as e:
        logger.error(f"Error reading VS Code extensions: {e}")
        return []


def get_vscode_workspace_info(directory: Path) -> Dict[str, any]:
    """
    Get VS Code workspace information including settings and extensions.
    
    Args:
        directory: The workspace directory
        
    Returns:
        Dict[str, any]: VS Code workspace information
    """
    return {
        "settings": get_vscode_settings(directory),
        "extensions": get_vscode_extensions(directory)
    }


def analyze_workspace_structure(directory: Path) -> Dict[str, any]:
    """
    Analyze the VSCode workspace structure to provide context for GitHub Copilot.
    
    Args:
        directory: The workspace directory
        
    Returns:
        Dict[str, any]: Workspace structure analysis
    """
    # Get basic files and directories
    try:
        top_level_items = list(directory.glob("*"))
        top_level_dirs = [item.name for item in top_level_items if item.is_dir() and not should_exclude(item, EXCLUDED_DIRS, set())]
        top_level_files = [item.name for item in top_level_items if item.is_file() and not should_exclude(item, set(), EXCLUDED_FILES)]
        
        # Get VSCode specific info
        vscode_info = get_vscode_workspace_info(directory)
        
        # Get information about package management and dependencies
        has_package_json = (directory / "package.json").exists()
        has_requirements_txt = (directory / "requirements.txt").exists()
        has_pipfile = (directory / "Pipfile").exists()
        has_poetry = (directory / "pyproject.toml").exists()
        has_docker = (directory / "Dockerfile").exists() or (directory / "docker-compose.yml").exists()
        
        return {
            "workspace_name": directory.name,
            "top_level_directories": top_level_dirs,
            "top_level_files": top_level_files,
            "vscode_info": vscode_info,
            "package_management": {
                "has_package_json": has_package_json,
                "has_requirements_txt": has_requirements_txt,
                "has_pipfile": has_pipfile,
                "has_poetry": has_poetry,
                "has_docker": has_docker
            }
        }
    except Exception as e:
        logger.error(f"Error analyzing workspace structure: {e}")
        return {"error": str(e)}


# ====================================================
# GitHub Copilot Specific Functions
# These functions help format data specifically for GitHub Copilot
# ====================================================

def get_github_copilot_ready_output(directory: Path, files_to_include: Optional[List[str]] = None) -> Dict[str, any]:
    """
    Generate a GitHub Copilot-ready object containing workspace analysis and file contents.
    
    Args:
        directory: Base workspace directory
        files_to_include: Optional list of specific files to include
        
    Returns:
        Dict[str, any]: Dictionary with workspace_info and file_contents
    """
    # Get workspace info
    workspace_info = analyze_workspace_structure(directory)
    
    # Get file contents
    if files_to_include:
        all_contents = {}
        all_files = get_file_contents(directory)
        
        for file_path in files_to_include:
            if file_path in all_files:
                all_contents[file_path] = all_files[file_path]
            else:
                # Try to find the file with a fuzzy match
                for path in all_files:
                    if file_path in path or path.endswith(file_path):
                        all_contents[path] = all_files[path]
                        break
    else:
        all_contents = get_file_contents(directory)
    
    # Format the result as a GitHub Copilot-ready object
    return {
        "workspace_info": workspace_info,
        "file_contents": all_contents
    }


def get_github_copilot_summary(directory: Path) -> Dict[str, any]:
    """
    Generate a summary of the workspace for GitHub Copilot, focusing on high-level structure.
    
    Args:
        directory: Base workspace directory
        
    Returns:
        Dict[str, any]: Dictionary with workspace summary information
    """
    try:
        # Get workspace structure info
        workspace_info = analyze_workspace_structure(directory)
        
        # Count files by language
        language_counts = {}
        for file_path in list_files(directory, EXCLUDED_DIRS, set()):
            try:
                language = detect_language(file_path)
                language_counts[language] = language_counts.get(language, 0) + 1
            except:
                pass
        
        # Get main project files
        important_files = []
        for name in ["main.py", "index.js", "app.py", "server.js", "package.json", "README.md", "requirements.txt"]:
            if (directory / name).exists():
                important_files.append(name)
        
        # Create the summary
        return {
            "workspace_name": workspace_info["workspace_name"],
            "important_files": important_files,
            "language_distribution": language_counts,
            "folder_structure": workspace_info["top_level_directories"],
            "vscode_extensions": workspace_info["vscode_info"]["extensions"],
            "package_management": workspace_info["package_management"]
        }
    except Exception as e:
        logger.error(f"Error generating GitHub Copilot summary: {e}")
        return {"error": str(e)}
