"""
config/agents.py

This module provides configurations for AI models used in different phases of analysis.
It allows users to easily configure which models to use for each phase by updating
the `MODEL_CONFIG` dictionary.

Users can specify a different model for each phase and whether to use reasoning.
"""

from core.types.models import (
    ModelConfig,
    AZURE_GPT4O_DEFAULT,
    AZURE_GPT4O_CREATIVE,
    AZURE_GPT4O_PRECISE,
    AZURE_GPT4_TURBO
)

# ====================================================
# Phase Model Configuration
# Define which model to use for each phase.
# ====================================================

# Default model configuration using Azure OpenAI
MODEL_CONFIG = {
    # Phase 1: Initial Discovery
    "phase1": AZURE_GPT4O_PRECISE,
    
    # Phase 2: Methodical Planning
    "phase2": AZURE_GPT4O_DEFAULT,
    
    # Phase 3: Deep Analysis
    "phase3": AZURE_GPT4O_DEFAULT,
    
    # Phase 4: Synthesis
    "phase4": AZURE_GPT4O_DEFAULT,
    
    # Phase 5: Consolidation
    "phase5": AZURE_GPT4O_CREATIVE,
    
    # Final Analysis
    "final": AZURE_GPT4O_PRECISE,
}
