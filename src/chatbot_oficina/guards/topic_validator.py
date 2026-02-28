"""Validador de tema para o chatbot de oficina."""
from typing import Tuple


ALLOWED_TOPICS = [
    "óleo", "oleo", "freio", "freios", "suspensão", "suspensao",
    "alinhamento", "balanceamento", "pneu", "pneus", "roda", "rodas",
    "motor", "câmbio", "cambio", "embreagem", "fluido", "filtro",
    "bateria", "alternador", "vela", "injecção", "injeção",
    "amortecedor", "mola", "pivô", "pivo", "terminal", "bieleta",
    "revisão", "revisao", "manutenção", "manutencao", "conserto",
    "troca", "serviço", "servico", "orçamento", "orcamento",
    "agendamento", "agendar", "horário", "horario", "funcionamento",
    "pagamento", "garantia", "peça", "peca", "valor", "preço", "preco",
    "veículo", "veiculo", "carro", "automotivo", "oficina", "mecânico",
    "mecanico", "diagnóstico", "diagnostico", "luz", "painel", "errado",
    "barulho", "vibração", "vibracao", "fumaça", "fumaca", "aquecimento",
    "eletrico", "elétrico", "arranque", "partida", "liga", "desliga"
]

REDIRECT_MESSAGE = (
    "Desculpe, só posso ajudar com dúvidas sobre serviços de oficina automotiva! "
    "Posso informar sobre serviços como: troca de óleo, alinhamento, balanceamento, "
    "freios, suspensão, diagnóstico, revisão, orçamentos, agendamento, etc. "
    "Como posso ajudar com seu veículo?"
)


def validate_topic(question: str) -> Tuple[bool, str]:
    """
    Valida se a pergunta está dentro do tema da oficina.
    
    Args:
        question: A pergunta do usuário
        
    Returns:
        Tuple[bool, str]: (é_válido, mensagem)
    """
    if not question or not question.strip():
        return False, REDIRECT_MESSAGE
    
    question_lower = question.lower()
    
    for topic in ALLOWED_TOPICS:
        if topic in question_lower:
            return True, ""
    
    return False, REDIRECT_MESSAGE
