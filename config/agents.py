"""
config/agents.py

This module provides configurations for AI models used in different phases of analysis.
It allows users to easily configure which models to use for each phase by updating
the `MODEL_CONFIG` dictionary.

Users can specify a different model for each phase and whether to use reasoning.
"""

from core.types.models import (
    ModelConfig,
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

# ====================================================
# Phase Model Configuration
# Define which model to use for each phase.
# ====================================================

# Default model configuration
MODEL_CONFIG = {
    # Phase 1: Initial Discovery
    "phase1": GPT4_1_PRECISE,
    
    # Phase 2: Methodical Planning
    "phase2": GEMINI_BASIC,
    
    # Phase 3: Deep Analysis
    "phase3": GEMINI_BASIC,
    
    # Phase 4: Synthesis
    "phase4": GEMINI_BASIC,
    
    # Phase 5: Consolidation
    "phase5": GEMINI_BASIC,
    
    # Final Analysis
    "final": GEMINI_BASIC,
}
