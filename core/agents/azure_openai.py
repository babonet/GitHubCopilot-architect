"""
core/agents/azure_openai.py

This module provides the AzureOpenAIArchitect class for interacting with Azure OpenAI models.
It handles the creation and execution of agent-based analysis using Azure OpenAI models.

This module is used by the main analysis process to perform specialized analysis tasks
with Azure OpenAI integration.
"""

# ====================================================
# Importing Necessary Libraries
# This section imports all the required libraries and modules.
# ====================================================

import json
import logging
import os
from typing import Dict, List, Optional, Any, Union
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential

from core.agents.base import BaseArchitect, ModelProvider, ReasoningMode
from config.prompts.phase_2_prompts import PHASE_2_PROMPT, format_phase2_prompt
from config.prompts.phase_4_prompts import PHASE_4_PROMPT, format_phase4_prompt
from config.prompts.final_analysis_prompt import FINAL_ANALYSIS_PROMPT, format_final_analysis_prompt

# ====================================================
# AzureOpenAIArchitect Class
# This class provides integration with Azure OpenAI models
# ====================================================

class AzureOpenAIArchitect(BaseArchitect):
    """
    Implements the BaseArchitect interface using Azure OpenAI models.
    This class handles communication with Azure OpenAI API endpoints and
    processes responses for code architecture analysis.
    """

    def __init__(self, model_config: Dict[str, Any], system_prompt: str = None):
        """
        Initialize the Azure OpenAI architect with configuration.
        
        Args:
            model_config: Configuration for the Azure OpenAI model
            system_prompt: Optional system prompt to use for all interactions
        """
        super().__init__(model_config=model_config, system_prompt=system_prompt)
          # Get Azure OpenAI configuration
        self.endpoint = os.environ.get("AZURE_ENDPOINT")
        self.api_key = os.environ.get("AZURE_API_KEY")
        self.api_version = "2024-12-01-preview"
        
        if not self.endpoint or not self.api_key:
            raise ValueError("AZURE_ENDPOINT and AZURE_API_KEY environment variables must be set")
            
        # Get deployment name from environment or use the one from model_config
        self.env_deployment = os.environ.get("AZURE_DEPLOYMENT")
        
        # Initialize the Azure OpenAI client
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.api_key
        )
          # Set model parameters from configuration
        # Use environment variable for deployment if available, otherwise use config
        self.deployment = self.env_deployment or model_config.get("deployment", "gpt-4o")
        self.model = model_config.get("model", "gpt-4o")
        self.max_tokens = model_config.get("max_tokens", 4096)
        self.temperature = model_config.get("temperature", 0.7)
        self.top_p = model_config.get("top_p", 0.95)
        self.provider = ModelProvider.AZURE_OPENAI
        self.reasoning_mode = model_config.get("reasoning_mode", ReasoningMode.MEDIUM)
    
    def get_provider(self) -> ModelProvider:
        """Get the model provider type."""
        return self.provider
    
    def get_reasoning_mode(self) -> ReasoningMode:
        """Get the reasoning mode being used."""
        return self.reasoning_mode
    
    async def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run analysis using the Azure OpenAI model.
        
        Args:
            context: Dictionary containing the context for analysis
            
        Returns:
            Dictionary containing the analysis results or error information
        """
        messages = [
            {
                "role": "system", 
                "content": self.system_message
            },
            {
                "role": "user", 
                "content": f"Analyze the following context: {json.dumps(context)}"
            }
        ]
        
        response = await self._call_azure_openai(messages)
        return {"analysis": response}
        
    async def analyze_project_phase_2(self, project_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze project structure for Phase 2.
        
        Args:
            project_structure: Project structure information
            
        Returns:
            Analysis results in a dictionary
        """
        prompt = format_phase2_prompt(PHASE_2_PROMPT, project_structure)
        
        # Create messages for chat completion
        messages = [
            {
                "role": "system",
                "content": self.system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Call Azure OpenAI API
        response = await self._call_azure_openai(messages)
        
        return {"analysis": response}
    
    async def analyze_project_phase_4(self, analyzed_files: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze project files for Phase 4.
        
        Args:
            analyzed_files: Dictionary of analyzed file content
            
        Returns:
            Analysis results in a dictionary
        """
        prompt = format_phase4_prompt(PHASE_4_PROMPT, analyzed_files)
        
        # Create messages for chat completion
        messages = [
            {
                "role": "system",
                "content": self.system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Call Azure OpenAI API
        response = await self._call_azure_openai(messages)
        
        return {"analysis": response}
    
    async def final_analysis(self, consolidated_report: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Perform final analysis on the consolidated report.
        
        Args:
            consolidated_report: Dictionary containing the consolidated report
            prompt: Optional custom prompt to use
            
        Returns:
            Dictionary containing the final analysis
        """
        user_prompt = prompt or f"Provide a final analysis of the consolidated report: {json.dumps(consolidated_report)}"
        
        messages = [
            {
                "role": "system", 
                "content": self.system_message
            },
            {
                "role": "user", 
                "content": user_prompt
            }
        ]
        
        response = await self._call_azure_openai(messages)
        return {"final_analysis": response}
    
    async def analyze_final(self, analyzed_files: Dict[str, Any], 
                            excluded_files: List[str]) -> Dict[str, Any]:
        """
        Perform final analysis.
        
        Args:
            analyzed_files: Dictionary of analyzed file content
            excluded_files: List of excluded files
            
        Returns:
            Final analysis results in a dictionary
        """
        prompt = format_final_analysis_prompt(FINAL_ANALYSIS_PROMPT, analyzed_files, excluded_files)
        
        # Create messages for chat completion
        messages = [
            {
                "role": "system",
                "content": self.system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Call Azure OpenAI API
        response = await self._call_azure_openai(messages)
        
        return {"analysis": response}
    
    async def create_analysis_plan(self, project_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an analysis plan based on project structure.
        
        Args:
            project_structure: Dictionary containing project structure
            
        Returns:
            Dictionary containing the analysis plan
        """
        messages = [
            {
                "role": "system", 
                "content": self.system_message
            },
            {
                "role": "user", 
                "content": f"Create an analysis plan for this project: {json.dumps(project_structure)}"
            }
        ]
        
        response = await self._call_azure_openai(messages)
        return {"plan": response}
    
    async def synthesize_findings(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize findings from analysis results.
        
        Args:
            analysis_results: Dictionary containing analysis results
            
        Returns:
            Dictionary containing synthesized findings
        """
        messages = [
            {
                "role": "system", 
                "content": self.system_message
            },
            {
                "role": "user", 
                "content": f"Synthesize the following analysis results: {json.dumps(analysis_results)}"
            }
        ]
        
        response = await self._call_azure_openai(messages)
        return {"synthesis": response}
    
    async def consolidate_results(self, all_results: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Consolidate results from all previous phases.
        
        Args:
            all_results: Dictionary containing all phase results
            prompt: Optional custom prompt to use
            
        Returns:
            Dictionary containing the consolidated report
        """
        user_prompt = prompt or f"Consolidate the following analysis results: {json.dumps(all_results)}"
        
        messages = [
            {
                "role": "system", 
                "content": self.system_message
            },
            {
                "role": "user", 
                "content": user_prompt
            }
        ]
        
        response = await self._call_azure_openai(messages)
        return {"consolidated_report": response}
    
    async def _call_azure_openai(self, messages: List[Dict[str, str]]) -> str:
        """
        Call the Azure OpenAI API with the given messages.
        
        Args:
            messages: List of message dictionaries to send to the API.
            
        Returns:
            The response content from the API.
        """
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                model=self.deployment
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error calling Azure OpenAI API: {e}")
            raise
    
    async def stream_call_azure_openai(self, messages: List[Dict[str, str]]) -> str:
        """
        Stream response from Azure OpenAI API.
        
        Args:
            messages: List of message dictionaries to send to the API.
            
        Returns:
            The complete response content from the API.
        """
        try:
            response = self.client.chat.completions.create(
                stream=True,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                model=self.deployment
            )
            
            collected_content = []
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    collected_content.append(content)
                    
                    # For streaming to console if needed
                    # print(content, end="", flush=True)
            
            return "".join(collected_content)
        except Exception as e:
            logging.error(f"Error streaming from Azure OpenAI API: {e}")
            raise
