from typing import List, Optional

from morph.core import Module

class ModelProvider(Module):
    """
    Base class for all LLM models.
    """

    def __init__(self, module_name: str = 'Model Provider', description: str = 'A LLM model provider that can manage interactions with LLM models.'):
        super().__init__(module_name, description)

    def generate(self, model_name: str, query: str) -> str:
        """
        Query the model with the given query.
        return: a string representing the model's response.
        """
        raise NotImplementedError
    
    def download_model(self, model_name: str):
        """
        Download the model with the given name.
        """
        raise NotImplementedError
    
    def remove_model(self, model_name: str):
        """
        Remove the model with the given name.
        """
        raise NotImplementedError
    
    def list_models(self) -> List[str]:
        """
        List all available models.
        """
        raise NotImplementedError
    
    def list_downloaded_models(self) -> List[str]:
        """
        List all downloaded models.
        """
        raise NotImplementedError
    
    def release_model(self, model_name: str):
        """
        Release the model with the given name.
        """
        raise NotImplementedError
