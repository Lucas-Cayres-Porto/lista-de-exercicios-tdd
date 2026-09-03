def avaliar_limite_credito(renda: float, possui_restricao: bool, score: int) -> float:
    """
    Avalia e calcula o limite de crédito aprovado para o cliente com base nas regras:
    - Renda < R$ 1.500,00 -> Limite: R$ 0,00
    - Restrição no CPF (True) -> Limite: R$ 0,00
    - Renda >= R$ 1.500,00 sem restrição -> Limite base = 30% da renda
    - Score > 800 -> Bônus de +50% sobre o limite base
    """
    pass