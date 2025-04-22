"""
core/agents/factory.py

This module provides a factory function for creating the appropriate architect 
instances based on configuration for different phases of analysis.

It serves as a central hub for instantiating the right architect implementation
based on the model configuration defined in config/agents.py.
"""

from typing import Any, Dict
from .base import ModelProvider, ReasoningMode
from .anthropic import AnthropicArchitect
from .openai import OpenAIArchitect
from .deepseek import DeepSeekArchitect
from .gemini import GeminiArchitect

def get_architect_for_phase(phase: str, **kwargs) -> Any:
    """
    Get the appropriate architect instance for a phase based on configuration.
    
    Args:
        phase: The phase to get an architect for (e.g., "phase1", "phase2")
        **kwargs: Additional keyword arguments to pass to the architect constructor
        
    Returns:
        An instance of the appropriate architect class for the specified phase
    """
    # Import here to avoid circular imports
    from config.agents import MODEL_CONFIG
    
    # Get model configuration for the phase
    config = MODEL_CONFIG.get(phase)
    if not config:
        raise ValueError(f"No model configuration found for phase '{phase}'")
    
    # Create the appropriate architect instance
    if config.provider == ModelProvider.ANTHROPIC:
        return AnthropicArchitect(
            model_name=config.model_name,
            reasoning=config.reasoning,
            **kwargs
        )
    elif config.provider == ModelProvider.OPENAI:
        return OpenAIArchitect(
            model_name=config.model_name,
            reasoning=config.reasoning,
            temperature=config.temperature,
            **kwargs
        )
    elif config.provider == ModelProvider.DEEPSEEK:
        # DeepSeek Reasoner has fixed parameters
        return DeepSeekArchitect(
            **kwargs  # Only pass the kwargs, other params are fixed in DeepSeekArchitect
        )
    elif config.provider == ModelProvider.GEMINI:
        return GeminiArchitect(
            model_name=config.model_name,
            reasoning=config.reasoning,
            **kwargs
        )
    else:
        raise ValueError(f"Unknown model provider: {config.provider}") 