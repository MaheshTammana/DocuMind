"""
Gemini API Client

Handles communication with Google's Gemini API for text generation.
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from typing import Optional

load_dotenv()


class GeminiClient:
    """Client for interacting with Google's Gemini API"""
    
    def __init__(self, model_name: str = 'gemini-1.5-flash'):
        """
        Initialize Gemini API client
        
        Args:
            model_name (str): Name of the Gemini model to use
                             Options: 'gemini-1.5-flash', 'gemini-1.5-pro'
        
        Raises:
            ValueError: If GEMINI_API_KEY is not found in environment
        """
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment. "
                "Please create a .env file with your API key."
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        
    def generate_text(
        self, 
        prompt: str, 
        temperature: float = 0.7, 
        max_tokens: int = 2048
    ) -> Optional[str]:
        """
        Generate text response from Gemini
        
        Args:
            prompt (str): Input prompt for generation
            temperature (float): Sampling temperature (0.0-1.0)
                               Lower = more focused, Higher = more creative
            max_tokens (int): Maximum tokens to generate
            
        Returns:
            str: Generated text response, or None if error occurs
        """
        try:
            generation_config = {
                'temperature': temperature,
                'max_output_tokens': max_tokens,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            print(f"Error generating text: {e}")
            return None
    
    def generate_with_retry(
        self, 
        prompt: str, 
        max_retries: int = 3,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Optional[str]:
        """
        Generate text with exponential backoff retry logic
        
        Handles rate limiting and transient errors automatically.
        
        Args:
            prompt (str): Input prompt for generation
            max_retries (int): Maximum number of retry attempts
            temperature (float): Sampling temperature
            max_tokens (int): Maximum tokens to generate
            
        Returns:
            str: Generated text response
            
        Raises:
            Exception: If all retry attempts fail
        """
        for attempt in range(max_retries):
            try:
                return self.generate_text(prompt, temperature, max_tokens)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                
                wait_time = 2 ** attempt
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
        
        return None
    
    def generate_streaming(self, prompt: str, temperature: float = 0.7):
        """
        Generate text with streaming response
        
        Yields chunks of text as they are generated.
        
        Args:
            prompt (str): Input prompt for generation
            temperature (float): Sampling temperature
            
        Yields:
            str: Chunks of generated text
        """
        try:
            generation_config = {
                'temperature': temperature,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            print(f"Error in streaming generation: {e}")
            yield f"Error: {str(e)}"
