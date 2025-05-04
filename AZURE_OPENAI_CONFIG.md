# Azure OpenAI Configuration Example

This file provides example configuration settings for Azure OpenAI integration with the GitHub Copilot Architect project.

## Environment Variables

```bash
# Linux/macOS
export AZURE_API_KEY='your-azure-api-key'
export AZURE_ENDPOINT='https://your-resource-name.openai.azure.com/'

# Windows PowerShell
$env:AZURE_API_KEY = 'your-azure-api-key'
$env:AZURE_ENDPOINT = 'https://your-resource-name.openai.azure.com/'

# Windows Command Prompt
set AZURE_API_KEY=your-azure-api-key
set AZURE_ENDPOINT=https://your-resource-name.openai.azure.com/
```

## Configuration File Example

```json
{
  "azure_openai": {
    "deployment": "gpt-4o",
    "model": "gpt-4o",
    "api_version": "2024-12-01-preview",
    "max_tokens": 4096,
    "temperature": 0.7,
    "top_p": 0.95
  },
  "architecture": {
    "vscode": {
      "extensions": [
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "ms-python.python",
        "ms-python.vscode-pylance"
      ],
      "settings": {
        "github.copilot.enable": {
          "*": true,
          "plaintext": true,
          "markdown": true,
          "python": true
        },
        "editor.formatOnSave": true,
        "python.linting.enabled": true
      }
    }
  }
}
```

## Azure OpenAI API Usage Example

```python
import os
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_key=os.environ["AZURE_API_KEY"]
)

# Generate a response
response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a code analysis assistant."
        },
        {
            "role": "user",
            "content": "Analyze this Python function: def hello(): print('Hello World')"
        }
    ],
    max_tokens=4096,
    temperature=0.7,
    model="gpt-4o"  # deployment name
)

print(response.choices[0].message.content)

# Stream a response
stream_response = client.chat.completions.create(
    stream=True,
    messages=[
        {
            "role": "system",
            "content": "You are a code analysis assistant."
        },
        {
            "role": "user",
            "content": "Suggest improvements for this Python function: def hello(): print('Hello World')"
        }
    ],
    max_tokens=4096,
    temperature=0.7,
    model="gpt-4o"  # deployment name
)

for chunk in stream_response:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```
