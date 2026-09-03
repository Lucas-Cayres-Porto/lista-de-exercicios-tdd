def avaliar_limite_credito(renda: float, possui_restricao: bool, score: int) -> float:
    """
    Avalia e calcula o limite de crédito aprovado com base no perfil financeiro.
    """
    # Regra 1 e Regra 2: Crédito negado se renda for menor que R$ 1.500 ou se tiver restrição no CPF
    if possui_restricao or renda < 1500.00:
        return 0.00

    # Regra 3: Limite base = 30% da renda mensal
    limite = renda * 0.30

    # Regra 4: Bônus de +50% se o score for acima de 800
    if score > 800:
        limite *= 1.50

    return limite