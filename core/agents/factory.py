"""
core/agents/factory.py

This module provides a factory function for creating the appropriate architect 
instances based on configuration for different phases of analysis.

It serves as a central hub for instantiating the right architect implementation
based on the model configuration defined in config/agents.py.
"""

from typing import Any, Dict
from .base import ModelProvider, ReasoningMode
from .azure_openai import AzureOpenAIArchitect

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
    if config.provider == ModelProvider.AZURE_OPENAI:
        return AzureOpenAIArchitect(
            model_config={
                "deployment": config.model_name,
                "model": config.model_name,
                "reasoning_mode": config.reasoning,
                "temperature": config.temperature,
                "max_tokens": kwargs.get("max_tokens", 4096),
                "top_p": kwargs.get("top_p", 0.95)
            },
            system_prompt=kwargs.get("system_prompt")
        )
    else:
        raise ValueError(f"Only Azure OpenAI provider is supported: {config.provider}")