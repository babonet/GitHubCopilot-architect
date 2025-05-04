"""
core/types package

This package contains type definitions for various components of the project.
"""

from .agent_config import AgentConfig
from .models import (
    ModelConfig,
    # Predefined Azure OpenAI model configurations
    AZURE_GPT4O_DEFAULT,
    AZURE_GPT4O_CREATIVE,
    AZURE_GPT4O_PRECISE,
    AZURE_GPT4_TURBO
)