from ollama import generate, pull, ListResponse, list, delete, show, ProcessResponse, ps, pull, embed
from tqdm import tqdm
from typing import List, Optional
import os

from morph.core.modelProviders import ModelProvider


class OllamaProvider(ModelProvider):
    """
    The OllamaModel class is a concrete implementation of the Model class.

    It provides an interface to the Ollama API (https://github.com/ollama/ollama-python/blob/main/ollama/_client.py)
    """
    
    def __init__(self, server_address: Optional[str] = None,module_name: str = 'Ollama Model Provider',description: str = 'Ollama is an open-source platform designed to simplify the deployment and operation of large language models (LLMs) locally on personal computers. Developed to empower users with privacy-focused, offline AI capabilities, it supports popular models like LLaMA, Mistral, and Gemma, allowing them to run efficiently on macOS, Linux, and Windows. Ollama provides a user-friendly command-line interface and a REST API, enabling developers and researchers to experiment with, customize, and integrate LLMs into applications without relying on cloud-based services. Its lightweight framework and Modelfile system—which lets users tweak model configurations—make it ideal for prototyping, AI-driven projects, or exploring LLM functionalities in a controlled environment. By prioritizing local execution, Ollama appeals to those seeking data security, reduced latency, and cost-effective AI experimentation.'):
        """
        Initialize the OllamaModel class.
        Args:
            server_address (Optional[str], optional): The address of the Ollama server. Defaults to None (connect to local Ollama server).
        """
        super().__init__(module_name, description)
        if server_address:
            os.environ["OLLAMA_HOST"] = server_address

    def start_ollama_server(self):
        """
        Start the Ollama server.
        """
        
        CONNECTION_ERROR_MESSAGE = 'Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible. https://ollama.com/download'
        
        raise NotImplementedError


    def generate(self, model_name, query: str) -> str:
        """
        Query the model with the given query.
        return: a string representing the model's response.
        """
        return generate(model_name, query)['response']

    
    def download_model(self, model_name: str):
        """
        Download the model with the given name.
        """
        current_digest, bars = '', {}
        for progress in pull(model_name, stream=True):
            digest = progress.get('digest', '')
            if digest != current_digest and current_digest in bars:
                bars[current_digest].close()

            if not digest:
                print(progress.get('status'))
                continue

            if digest not in bars and (total := progress.get('total')):
                bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)

            if completed := progress.get('completed'):
                bars[digest].update(completed - bars[digest].n)

        current_digest = digest
    
    def remove_model(self, model_name: str):
        """
        Remove the model with the given name.
        """
        delete(model_name)
    
    def list_models(self) -> List[str]:
        """
        List all available models.
        """
        raise NotImplementedError
    
    def list_downloaded_models(self):
        """
        List all downloaded models.
        """
        response: ListResponse = list()

        for model in response.models:
            print('Name:', model.model)
            print('  Size (MB):', f'{(model.size.real / 1024 / 1024):.2f}')
            if model.details:
                print('  Format:', model.details.format)
                print('  Family:', model.details.family)
                print('  Parameter Size:', model.details.parameter_size)
                print('  Quantization Level:', model.details.quantization_level)
            print('\n')
    
    def show_model_details(self, model_name):
        """Show details of a specific local model"""
        response = show(model_name)
        print('Name:', model_name)
        print('  Format:', response.details.format)
        print('  Family:', response.details.family)
        print('  Parameter Size:',response.details.parameter_size)
        print('  Quantization Level:', response.details.quantization_level)
        print('\n')


    def ps(self):
        """List all running processes"""
        response: ProcessResponse = ps()
        if response.models:
            for model in response.models:
                print('Model: ', model.model)
                print('  Digest: ', model.digest)
                print('  Expires at: ', model.expires_at)
                print('  Size: ', model.size)
                print('  Size vram: ', model.size_vram)
                print('  Details: ', model.details)
                print('\n')

    def embed(self, model_name: str, query: str):
        response = embed(model=model_name, input=query)
        print(response['embeddings'])

    def release_model(self, model_name: str):
        """
        Release the model with the given name.
        """
        raise NotImplementedError
