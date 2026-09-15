"""
Shared LLM client for OpenRouter integration
Used by both Farmer Assistant and Agentic Advisor
"""

import requests
import logging
from typing import Dict, List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for OpenRouter API using Qwen model"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.api_url = settings.OPENROUTER_API_URL
        
    def _make_request(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[str]:
        """Make request to OpenRouter API"""
        
        if not self.api_key:
            logger.error("OPENROUTER_API_KEY not configured")
            return None
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://agrismart-ai.com",  # Optional
            "X-Title": "Agrismart AI"  # Optional
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.Timeout:
            logger.error("OpenRouter API timeout")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"OpenRouter API HTTP error: {e}")
            return None
        except KeyError as e:
            logger.error(f"Unexpected OpenRouter API response format: {e}")
            return None
        except Exception as e:
            logger.error(f"OpenRouter API error: {e}")
            return None
    
    def chat(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        Send a chat request to the LLM
        
        Args:
            system_prompt: System instructions
            user_message: User's question/message
            temperature: Sampling temperature
            max_tokens: Maximum response length
            
        Returns:
            LLM response or None if failed
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        return self._make_request(messages, temperature, max_tokens)
    
    def generate_explanation(
        self,
        decision: str,
        reason: str,
        context: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Generate farmer-friendly explanation for a decision
        
        Args:
            decision: The action/decision made
            reason: Technical reason for the decision
            context: Optional farm context
            
        Returns:
            Farmer-friendly explanation or None if failed
        """
        system_prompt = """You are an agricultural advisor. 
Explain technical farming decisions in simple, friendly language.
Keep responses concise (2-3 sentences).
Use emojis sparingly to make it friendly."""
        
        user_message = f"Decision: {decision}\nReason: {reason}"
        if context:
            user_message += f"\nContext: {context}"
        
        return self.chat(
            system_prompt=system_prompt,
            user_message=user_message,
            temperature=0.5,
            max_tokens=200
        )


# Global instance
llm_client = LLMClient()
