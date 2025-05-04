# Adapting the CursorRules Architect for VSCode and GitHub Copilot

Based on the codebase analysis, here's what you'll need to modify to adapt this project for VSCode with GitHub Copilot and Azure AI exclusively:

## 1. Core Changes Required

### Replace `.cursorrules` with VSCode-compatible Format

You already have a `.vscode` folder, so you'll need to:

1. Update GitHub Copilot configuration in your existing `.vscode` directory
2. Update documentation to reference GitHub Copilot instead of CursorRules

### Update API Integration

Since you'll exclusively use Azure AI:

1. Remove integration code for Anthropic, OpenAI, DeepSeek, and Google Gemini
2. Add Azure OpenAI SDK integration and authentication based on the AzureAISample.md reference
3. Update model references to Azure AI available models (e.g., gpt-4o)

### Configuration Updates

Update configuration and environment setup:

1. Replace Cursor-specific environment variables with Azure AI equivalents (AZURE_API_KEY, azure_endpoint)
2. Update installation instructions for VSCode and GitHub Copilot

## 2. Detailed Implementation Plan

### Step 1: Update `.vscode` Configuration

Update your existing `.vscode/settings.json` file to include GitHub Copilot settings:

```json
{
    "github.copilot.enable": {
        "*": true,
        "plaintext": true,
        "markdown": true,
        "python": true
    }
}
```

### Step 2: Update `README.md`

Update the README to reflect the new tooling:

```markdown
# 🦊 GitHub Copilot Architect

**Your Azure AI-powered Code Analysis and Architecture Generator 🚀**

[Features](#-features) • [Requirements](#-requirements) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#-configuration) • [Architecture](#-architecture) • [Output](#-output) • [Contributing](#-contributing)

## 🛠️ Requirements

- Python 3.8+
- Visual Studio Code with GitHub Copilot extension
- Azure AI API key with access to appropriate models
- Dependencies:
  - `azure-ai-ml` for Azure AI API access
  - `rich` for beautiful terminal output
  - `click` for CLI interface
  - `pathlib` for path manipulation
  - `asyncio` for async operations

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/githubcopilot-architect.git
   cd githubcopilot-architect
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Keys**
   ```bash
   # Linux/macOS
   export AZURE_API_KEY='your-azure-api-key'
   export AZURE_ENDPOINT='your-azure-endpoint'

   # Windows
   set AZURE_API_KEY=your-azure-api-key
   set AZURE_ENDPOINT=your-azure-endpoint
   ```
```

### Step 3: Update `Requirements.txt`

Update the requirements file to include Azure OpenAI SDK dependencies based on the AzureAISample.md reference:

```plaintext
openai>=1.2.0
azure-identity>=1.12.0
azure-core>=1.26.0
rich>=13.3.5
click>=8.1.3
pathlib>=1.0.1
asyncio>=3.4.3
```

### Step 4: Update `CONTRIBUTING.md`

Modify the contribution guidelines:

```markdown
# Contributing to GitHub Copilot Architect

Thank you for considering contributing to GitHub Copilot Architect! Your help is greatly appreciated. This guide explains how you can contribute to the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Azure AI API key with access to appropriate models
- Visual Studio Code with GitHub Copilot extension
- Git

### Installing Dependencies

Clone the repository:

```bash
git clone https://github.com/yourusername/githubcopilot-architect.git
cd githubcopilot-architect
```

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### Setting Up API Keys

For development, you'll need to set up your Azure AI API key:

```bash
# Linux/macOS
export AZURE_API_KEY='your-azure-api-key' 
export AZURE_ENDPOINT='your-azure-endpoint'

# Windows
set AZURE_API_KEY=your-azure-api-key
set AZURE_ENDPOINT=your-azure-endpoint
```
```

### Step 5: Create Azure OpenAI Integration Module

Create a base architect for Azure OpenAI based on the AzureAISample.md reference:

```python
"""
Azure OpenAI Integration for the GitHub Copilot Architect.

This module provides integration with Azure OpenAI services for code analysis
and architecture generation.
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from pathlib import Path

from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential

from ..base_architect import BaseArchitect

class AzureArchitect(BaseArchitect):
    """
    Implementation of the BaseArchitect using Azure OpenAI services.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Azure OpenAI architect with the given configuration.
        
        Args:
            config: Dictionary containing configuration parameters.
        """
        super().__init__(config)
        self.api_key = os.environ.get("AZURE_API_KEY")
        self.endpoint = os.environ.get("AZURE_ENDPOINT")
        self.api_version = "2024-12-01-preview"
        
        if not self.api_key or not self.endpoint:
            raise ValueError("AZURE_API_KEY and AZURE_ENDPOINT environment variables must be set")
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.api_key
        )
        
        # Default model deployment to use
        self.model = config.get("model", "gpt-4o")
        self.deployment = config.get("deployment", "gpt-4o")

    async def analyze_project(self, project_path: Path) -> Dict[str, Any]:
        """
        Analyze the project at the given path using Azure OpenAI.
        
        Args:
            project_path: Path to the project directory.
            
        Returns:
            Dictionary containing analysis results.
        """
        # Implementation for project analysis using the chat completions API
        project_files = self._gather_project_files(project_path)
        
        # Create analysis prompt
        messages = [
            {
                "role": "system",
                "content": "You are a code analysis assistant that analyzes project structures and provides architecture recommendations."
            },
            {
                "role": "user",
                "content": f"Analyze the following project structure and files: {json.dumps(project_files)}"
            }
        ]
        
        # Call Azure OpenAI API
        response = await self._call_azure_openai(messages)
        return {"analysis": response}
    
    async def generate_architecture(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate architecture recommendations based on analysis results.
        
        Args:
            analysis_results: Dictionary containing analysis results.
            
        Returns:
            Dictionary containing architecture recommendations.
        """
        # Implementation for architecture generation using the chat completions API
        messages = [
            {
                "role": "system",
                "content": "You are an architecture assistant that provides recommendations based on code analysis."
            },
            {
                "role": "user",
                "content": f"Generate architecture recommendations based on this analysis: {analysis_results['analysis']}"
            }
        ]
        
        # Call Azure OpenAI API
        response = await self._call_azure_openai(messages)
        return {"recommendations": response}
    
    async def _call_azure_openai(self, messages: List[Dict[str, str]]) -> str:
        """
        Call the Azure OpenAI API with the given messages.
        
        Args:
            messages: List of message dictionaries to send to the API.
            
        Returns:
            The response content from the API.
        """
        response = self.client.chat.completions.create(
            messages=messages,
            max_tokens=4096,
            temperature=0.7,
            top_p=0.95,
            model=self.deployment
        )
        
        return response.choices[0].message.content
    
    def _gather_project_files(self, project_path: Path) -> Dict[str, Any]:
        """
        Gather information about project files.
        
        Args:
            project_path: Path to the project directory.
            
        Returns:
            Dictionary containing information about project files.
        """
        # Implementation to gather project files
        # This would scan the directory and collect relevant code files
        pass

    async def create_vscode_settings(self, architecture: Dict[str, Any], output_path: Path) -> None:
        """
        Create VSCode settings based on the generated architecture.
        
        Args:
            architecture: Dictionary containing architecture recommendations.
            output_path: Path where the VSCode settings should be saved.
        """
        # Implementation for VSCode settings generation
        settings_dir = output_path / ".vscode"
        settings_dir.mkdir(exist_ok=True)
        
        settings = {
            "github.copilot.enable": {
                "*": True,
                "plaintext": True,
                "markdown": True,
                "python": True
            },
            # Additional settings based on architecture
        }
        
        with open(settings_dir / "settings.json", "w") as f:
            json.dump(settings, f, indent=4)
```

## 3. Security and Dependency Considerations

Based on the analysis report, address these critical issues:

1. Implement strict file access whitelist for static file serving
2. Disable debug mode in non-development environments
3. Setup HTTPS/TLS support for any web components
4. Create a version-locked `requirements.txt` file with Azure OpenAI specific dependencies:

```plaintext
# Azure OpenAI dependencies
openai==1.2.0
azure-identity==1.12.0
azure-core==1.26.0

# Existing dependencies with locked versions
rich==13.3.5
click==8.1.3
pathlib==1.0.1
asyncio==3.4.3
```

5. Implement proper error handling for Azure OpenAI API calls
6. Store API keys securely using environment variables or Azure Key Vault

These security considerations were highlighted in the project analysis report and should be maintained in your adaptation.

## 4. Implementation of the Azure OpenAI Client

Based on the AzureAISample.md reference, implement the main Azure OpenAI client in a new file:

```python
# core/agents/azure_openai.py

import os
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from typing import Dict, List, Any, Optional

from .base import BaseAgent

class AzureOpenAIAgent(BaseAgent):
    """Agent implementation using Azure OpenAI API."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the Azure OpenAI agent with configuration."""
        super().__init__(config)
        
        self.endpoint = os.environ.get("AZURE_ENDPOINT")
        self.api_key = os.environ.get("AZURE_API_KEY")
        self.api_version = "2024-12-01-preview"
        
        if not self.endpoint or not self.api_key:
            raise ValueError("AZURE_ENDPOINT and AZURE_API_KEY must be set in environment variables")
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.api_key
        )
        
        self.deployment = config.get("deployment", "gpt-4o")
        self.model = config.get("model", "gpt-4o")
        self.max_tokens = config.get("max_tokens", 4096)
        self.temperature = config.get("temperature", 0.7)
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using Azure OpenAI."""
        messages = [
            {
                "role": "system",
                "content": self.system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.client.chat.completions.create(
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            model=self.deployment
        )
        
        return response.choices[0].message.content
    
    async def stream(self, prompt: str, **kwargs) -> str:
        """Stream a response using Azure OpenAI."""
        messages = [
            {
                "role": "system",
                "content": self.system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.client.chat.completions.create(
            stream=True,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            model=self.deployment
        )
        
        collected_content = []
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                collected_content.append(content)
                
                # For streaming to console if needed
                # print(content, end="", flush=True)
        
        return "".join(collected_content)
```

## 5. Next Steps

1. Update the `core/agents/factory.py` to initialize the Azure OpenAI agent instead of multiple providers
2. Remove Anthropic, OpenAI (non-Azure), DeepSeek, and Google Gemini agent implementations
3. Revise all documentation to reference VSCode and GitHub Copilot
4. Update configuration files to use Azure OpenAI models
5. Test the integration with Azure OpenAI models
6. Update unit tests to use Azure OpenAI mocks
7. Modify the file_retriever.py to work with VSCode instead of Cursor

This adaptation preserves the core functionality while shifting from CursorRules to VSCode with GitHub Copilot and focusing exclusively on Azure OpenAI integration.
