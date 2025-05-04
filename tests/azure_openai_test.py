
"""
Test script for Azure OpenAI integration.

This script tests the connection to Azure OpenAI API by creating
an architect instance and making a simple request.

Usage:
    python -m tests.azure_openai_test
"""

import os
import asyncio
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI

# Add the project root to the path to resolve imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import our modules
from core.agents.azure_openai import AzureOpenAIArchitect
from core.types.models import ReasoningMode

def print_color(text, color="green"):
    """Print colored text to the console."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

async def test_azure_openai():
    """Test the Azure OpenAI integration."""
    # Load environment variables
    load_dotenv()
    
    # Check if the required environment variables are set
    azure_endpoint = os.environ.get("AZURE_ENDPOINT")
    azure_api_key = os.environ.get("AZURE_API_KEY")
    
    if not azure_endpoint or not azure_api_key:
        print_color("Error: AZURE_ENDPOINT and AZURE_API_KEY must be set in .env file", "red")
        return False
        print_color("Azure OpenAI environment variables found", "green")
    
    try:
        # Create an instance of AzureOpenAIArchitect
        deployment = os.environ.get("AZURE_DEPLOYMENT", "gpt-4o")
        model_config = {
            "deployment": deployment,
            "model": "gpt-4o",
            "reasoning_mode": ReasoningMode.MEDIUM,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        architect = AzureOpenAIArchitect(
            model_config=model_config,
            system_prompt="You are a code analysis assistant."
        )
        
        print_color("Successfully created AzureOpenAIArchitect instance", "green")
        
        # Test a simple query
        messages = [
            {
                "role": "system",
                "content": "You are a code analysis assistant."
            },
            {
                "role": "user",
                "content": "What are the best practices for structuring a Python project?"
            }
        ]
        
        print_color("Sending test query to Azure OpenAI...", "blue")
        response = await architect._call_azure_openai(messages)
        
        print_color("\nResponse from Azure OpenAI:", "yellow")
        print(response)
        
        return True
    
    except Exception as e:
        print_color(f"Error: {e}", "red")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_azure_openai())
    if success:
        print_color("\nAzure OpenAI integration test completed successfully!", "green")
    else:
        print_color("\nAzure OpenAI integration test failed!", "red")
        sys.exit(1)
