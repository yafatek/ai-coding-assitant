import uuid
from typing import List, Dict, Any

import google.generativeai as genai
from google.api_core import retry

from loggers.Logger import Logger
from memory.redis_memory import RedisMemory
from prompts import SOFTWARE_DEVELOPER
from tools.tools import search_custom_engine, scrape_website

logger = Logger()

default_safety = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]


class CodingAgent:
    def __init__(self,
                 api_key: str,
                 model_name='gemini-1.5-pro', system_instruction=SOFTWARE_DEVELOPER, memory=RedisMemory(),
                 chat_id: str = None):
        """
        Initializes the CodingAgent with the given parameters.
        Args:
            model_name: The name of the Generative Model to use.
            system_instruction: The system instruction for the model.
        """
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.safety_settings = default_safety
        self.memory = memory
        self.chat_id = chat_id
        self.tools = [search_custom_engine, scrape_website]
        self.convo = None
        genai.configure(api_key=api_key)  # Replace with your actual API key

    @staticmethod
    def _format_history_for_gemini(history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Formats conversation history from memory to be compatible with Gemini's expected format.
        Args:
            history (List[Dict[str, Any]]): History in the memory's format.
        Returns:
            List[Dict[str, Any]]: History formatted for Gemini.
        """
        return [{"role": msg["role"], "parts": [{"text": msg["content"]}]} for msg in history]

    async def _load_memory(self) -> List[Dict[str, Any]]:
        """
        Loads conversation history from the memory object.
        Returns:
            List[Dict[str, Any]]: List of conversation turns in Gemini's format.
        """
        history = await self.memory.get_items(self.chat_id)
        return self._format_history_for_gemini(history[:10])

    async def _store_interaction(self, user_message: str, model_response: str) -> None:
        """
        Stores a user message and the model's response in memory.
        Args:
            user_message (str): The user's message.
            model_response (str): The model's response.
        """
        await self.memory.add_item(self.chat_id, {"role": "user", "content": user_message})
        await self.memory.add_item(self.chat_id, {"role": "model", "content": model_response})

    def _create_conversation(self) -> Any:
        """
        Creates a new conversation with the specified model and configuration.
        Returns:
            Any: Gemini conversation object.
        """
        model = genai.GenerativeModel(
            self.model_name,
            system_instruction=self.system_instruction,
            safety_settings=self.safety_settings,  # Use instance safety settings
            tools=self.tools,
        )
        return model.start_chat(enable_automatic_function_calling=True)

    def initialize_chat(self) -> None:
        """
        Initializes a new chat session with the Gemini model.
        """
        if not self.convo:
            self.convo = self._create_conversation()
            logger.info(f"Initialized chat for {self.__class__.__name__}, chat ID: {self.chat_id}")

    async def generate_code(self, prompt):
        """
        Generates code based on the given prompt.
        Args:
            prompt: The prompt to generate code from.
        Returns:
            The generated code.
        """
        if not self.convo:
            self.initialize_chat()

        if self.memory:
            self.convo.history = await self._load_memory()  # Load history from memory
        logger.info(f'[*] history len: {len(self.convo.history)}')
        response = await self.convo.send_message_async(
            prompt,
            request_options={'retry': retry.AsyncRetry()}  # Add retry logic for robustness
        )
        logger.info(response.usage_metadata)  # Print usage metadata (token consumption, etc.)
        if self.memory:
            logger.info(f'[*] to memory')
            await self._store_interaction(prompt, response.text)  # Store the interaction in memory

        return response.text  # Return the model's response text
