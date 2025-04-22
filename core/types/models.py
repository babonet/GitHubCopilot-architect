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

CLAUDE_BASIC = ModelConfig(
    provider=ModelProvider.ANTHROPIC,
    model_name="claude-3-7-sonnet-20250219",
    reasoning=ReasoningMode.DISABLED
)

CLAUDE_WITH_REASONING = ModelConfig(
    provider=ModelProvider.ANTHROPIC,
    model_name="claude-3-7-sonnet-20250219",
    reasoning=ReasoningMode.ENABLED
)

# O1 configurations with different reasoning levels
O1_HIGH = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o1",
    reasoning=ReasoningMode.HIGH
)

O1_MEDIUM = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o1",
    reasoning=ReasoningMode.MEDIUM
)

O1_LOW = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o1",
    reasoning=ReasoningMode.LOW
)

# O3-mini configurations with different reasoning levels
O3_MINI_HIGH = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o3-mini",
    reasoning=ReasoningMode.HIGH
)

O3_MINI_MEDIUM = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o3-mini",
    reasoning=ReasoningMode.MEDIUM
)

O3_MINI_LOW = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o3-mini",
    reasoning=ReasoningMode.LOW
)

# gpt-4.1 configurations with different temperature values
GPT4_1_DEFAULT = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="gpt-4.1",
    reasoning=ReasoningMode.TEMPERATURE,
    temperature=0.7  # Default temperature
)

GPT4_1_CREATIVE = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="gpt-4.1",
    reasoning=ReasoningMode.TEMPERATURE,
    temperature=0.9  # Higher temperature for more creative outputs
)

GPT4_1_PRECISE = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="gpt-4.1",
    reasoning=ReasoningMode.TEMPERATURE,
    temperature=0.2  # Lower temperature for more precise/deterministic outputs
)

# DeepSeek configurations
DEEPSEEK_REASONER = ModelConfig(
    provider=ModelProvider.DEEPSEEK,
    model_name="deepseek-reasoner",
    reasoning=ReasoningMode.ENABLED  # Always enabled for reasoner
)

# Gemini configurations
GEMINI_BASIC = ModelConfig(
    provider=ModelProvider.GEMINI,
    model_name="gemini-2.5-flash-preview-04-17",
    reasoning=ReasoningMode.DISABLED
)

GEMINI_WITH_REASONING = ModelConfig(
    provider=ModelProvider.GEMINI,
    model_name="gemini-2.5-pro-preview-03-25",
    reasoning=ReasoningMode.ENABLED
) 