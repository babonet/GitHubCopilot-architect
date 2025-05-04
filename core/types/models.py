"""
core/types/models.py

This module defines the model configuration types and predefined model configurations
used throughout the CursorRules Architect system.
"""

from typing import Dict, Any, NamedTuple, Optional
from core.agents.base import ModelProvider, ReasoningMode

# ====================================================
# Model Configuration Types
# This section defines types for model configuration.
# ====================================================

class ModelConfig(NamedTuple):
    """Configuration for a specific AI model."""
    provider: ModelProvider
    model_name: str
    reasoning: ReasoningMode = ReasoningMode.DISABLED
    temperature: Optional[float] = None  # For temperature-based models like gpt-4.1

# ====================================================
# Predefined Model Configurations
# These are shorthand configurations that can be referenced in the MODEL_CONFIG.
# ====================================================

# ====================================================
# Azure OpenAI Model Configurations
# These are configurations specifically for Azure OpenAI models
# ====================================================

AZURE_GPT4O_DEFAULT = ModelConfig(
    provider=ModelProvider.AZURE_OPENAI,
    model_name="gpt-4o",
    reasoning=ReasoningMode.MEDIUM,
    temperature=0.7
)

AZURE_GPT4O_CREATIVE = ModelConfig(
    provider=ModelProvider.AZURE_OPENAI,
    model_name="gpt-4o",
    reasoning=ReasoningMode.MEDIUM,
    temperature=0.9
)

AZURE_GPT4O_PRECISE = ModelConfig(
    provider=ModelProvider.AZURE_OPENAI,
    model_name="gpt-4o",
    reasoning=ReasoningMode.HIGH,
    temperature=0.3
)

# For more powerful versions if available in your Azure subscription
AZURE_GPT4_TURBO = ModelConfig(
    provider=ModelProvider.AZURE_OPENAI,
    model_name="gpt-4-turbo",
    reasoning=ReasoningMode.MEDIUM,
    temperature=0.7
)