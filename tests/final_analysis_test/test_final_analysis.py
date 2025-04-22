"""
tests/final_analysis/test_final_analysis.py

This script tests the Final Analysis phase of the CursorRules Architect.
It verifies that the Final Analysis works correctly with different model configurations.
"""

import sys
import os
import asyncio
import json
from typing import Dict
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.analysis.final_analysis import FinalAnalysis
from core.types.models import (
    CLAUDE_WITH_REASONING, 
    O1_HIGH, 
    GPT4_1_DEFAULT as GPT4_1, 
    O3_MINI_HIGH,
    ModelConfig
)
from config.agents import MODEL_CONFIG
from core.agents import get_architect_for_phase
from core.agents.base import ModelProvider, ReasoningMode

# Sample consolidated report for testing
SAMPLE_CONSOLIDATED_REPORT = {
    "project_name": "Test Project",
    "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    "phases": {
        "phase1": {
            "structure": {
                "findings": "The project has a clear structure with modules X, Y, Z."
            },
            "dependency": {
                "findings": "The project uses libraries A, B, C."
            },
            "tech_stack": {
                "findings": "The project is built with Python using Framework D."
            }
        },
        "phase4": {
            "analysis": "The project follows a clear architectural pattern with good separation of concerns."
        },
        "phase5": {
            "consolidated_findings": "This is a well-structured project with clear architecture."
        }
    }
}

# Sample project structure for testing
SAMPLE_PROJECT_STRUCTURE = [
    ".",
    "├── main.py",
    "├── config/",
    "│   ├── __init__.py",
    "│   └── settings.py",
    "├── core/",
    "│   ├── __init__.py",
    "│   ├── models.py",
    "│   └── utils.py",
    "└── tests/",
    "    ├── __init__.py",
    "    └── test_main.py"
]

async def test_model_config(model_config: ModelConfig, model_name: str):
    """Test the final analysis with a specific model configuration."""
    print(f"\n\nTesting with {model_name}: {model_config.provider.value} - {model_config.model_name}")
    print("-" * 50)
    
    # Override the MODEL_CONFIG for this test
    import config.agents
    original_config = config.agents.MODEL_CONFIG.get("final")
    config.agents.MODEL_CONFIG["final"] = model_config
    
    try:
        # Initialize the FinalAnalysis class
        final_analysis = FinalAnalysis()
        
        # Run the final analysis
        start_time = datetime.now()
        result = await final_analysis.run(SAMPLE_CONSOLIDATED_REPORT, SAMPLE_PROJECT_STRUCTURE)
        end_time = datetime.now()
        
        # Check if the result is valid
        if "status" in result and result["status"] == "error":
            print(f"❌ ERROR: {result.get('error', 'Unknown error')}")
            return False
        
        # Check if the result contains the expected keys
        expected_keys = ["output", "tokens_used"]
        if all(key in result for key in expected_keys):
            print(f"✅ PASSED: The final analysis returned the expected keys")
        else:
            print(f"❌ FAILED: The final analysis did not return all expected keys. Got: {list(result.keys())}")
            return False
        
        # Print some information about the result
        print(f"Time taken: {end_time - start_time}")
        print(f"Tokens used: {result.get('tokens_used', 'Not available')}")
        
        # Print a sample of the output
        output_sample = result.get("output", "")[:200] + "..." if result.get("output") else "No output"
        print(f"Output sample: {output_sample}")
        
        return True
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False
    finally:
        # Restore the original configuration
        config.agents.MODEL_CONFIG["final"] = original_config

async def run_all_tests():
    """Run tests with all available model configurations."""
    # Tests to run
    models_to_test = [
        ("CLAUDE_WITH_REASONING", CLAUDE_WITH_REASONING),
        ("O1_HIGH", O1_HIGH),
        ("GPT4_1", GPT4_1),
        ("O3_MINI_HIGH", O3_MINI_HIGH)
    ]
    
    # Current model from MODEL_CONFIG
    current_model = MODEL_CONFIG.get("final")
    current_model_name = "DEFAULT_CONFIG"
    
    # Also test the current model from MODEL_CONFIG
    if current_model:
        models_to_test.append((current_model_name, current_model))
    
    # Run all tests
    results = {}
    for model_name, model_config in models_to_test:
        results[model_name] = await test_model_config(model_config, model_name)
    
    # Print summary
    print("\n\nTest Summary:")
    print("=" * 50)
    for model_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        print(f"{model_name}: {status}")
    
    # Calculate overall status
    overall_status = all(results.values())
    print(f"\nOverall status: {'PASSED' if overall_status else 'FAILED'}")

if __name__ == "__main__":
    asyncio.run(run_all_tests()) 