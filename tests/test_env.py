#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import sys

# Load environment variables from .env file if it exists
print("Checking for .env file...")
if os.path.exists('.env'):
    print("Found .env file, loading environment variables...")
    load_dotenv()
    print("Environment variables loaded from .env file")
else:
    print("No .env file found.")

# Check if Azure OpenAI API keys are set
api_keys = {
    "AZURE_OPENAI_API_KEY": os.environ.get("AZURE_OPENAI_API_KEY"),
    "AZURE_OPENAI_ENDPOINT": os.environ.get("AZURE_OPENAI_ENDPOINT")
}

print("\nAPI Key Status:")
for key_name, key_value in api_keys.items():
    if key_value:
        masked_key = key_value[:4] + "*" * (len(key_value) - 8) + key_value[-4:] if len(key_value) > 8 else "****"
        print(f"✓ {key_name} is set: {masked_key}")
    else:
        print(f"✗ {key_name} is not set")

print("\nEnvironment test complete.") 