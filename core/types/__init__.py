"""
core/types package

This package contains type definitions for various components of the project.
"""

from .agent_config import AgentConfig
from .models import (
    ModelConfig,
    # Predefined model configurations
    CLAUDE_BASIC,
    CLAUDE_WITH_REASONING,
    O1_HIGH,
    O1_MEDIUM,
    O1_LOW,
    O3_MINI_HIGH, 
    O3_MINI_MEDIUM,
    O3_MINI_LOW,
    GPT4_1_DEFAULT,
    GPT4_1_CREATIVE,
    GPT4_1_PRECISE,
    DEEPSEEK_REASONER,
    GEMINI_BASIC,
    GEMINI_WITH_REASONING
) 