"""Detector de prompt injection."""
from typing import Tuple


INJECTION_PATTERNS = [
    "ignore previous",
    "ignore all",
    "disregard",
    "system prompt",
    "you are now",
    "pretend to be",
    "act as",
    "roleplay",
    "new instructions",
    "override",
    "bypass",
    "forget everything",
    "forget your",
    "new persona",
    "respond in the style",
    "output the following",
    "ignore instructions",
    "disobey",
    "not following",
    "instead respond",
    "forget the rules",
    "new rules",
    "modify your",
    "change your",
    "you are free",
    "no restrictions",
    "without limitations",
    "```json",
    "```xml",
    "<xml>",
    "<json>",
    "eval(",
    "exec(",
    "import os",
    "import sys",
    "subprocess",
    "os.system",
    "password",
    "api_key",
    "secret",
    "token"
]

INJECTION_MESSAGE = (
    "Desculpe, não posso processar essa solicitação. "
    "Posso ajudar apenas com dúvidas sobre serviços da oficina automotiva. "
    "Como posso ajudar com seu veículo hoje?"
)


def detect_injection(question: str) -> Tuple[bool, str]:
    """
    Detecta tentativas de prompt injection.
    
    Args:
        question: A pergunta do usuário
        
    Returns:
        Tuple[bool, str]: (é_injeção, mensagem)
    """
    if not question or not question.strip():
        return False, ""
    
    question_lower = question.lower()
    
    for pattern in INJECTION_PATTERNS:
        if pattern in question_lower:
            return True, INJECTION_MESSAGE
    
    return False, ""
