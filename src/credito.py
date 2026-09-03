# Constantes de Política de Crédito
RENDA_MINIMA_APROVACAO: float = 1500.00
PERCENTUAL_LIMITE_BASE: float = 0.30
SCORE_MINIMO_BONUS: int = 800
FATOR_BONUS_SCORE_ALTO: float = 1.50


def avaliar_limite_credito(renda: float, possui_restricao: bool, score: int) -> float:
    """
    Avalia e calcula o limite de crédito aprovado com base no perfil financeiro.

    Regras de Negócio:
        - Renda < R$ 1.500,00 -> Limite: R$ 0,00
        - Restrição no CPF -> Limite: R$ 0,00
        - Renda >= R$ 1.500,00 sem restrição -> Limite base = 30% da renda mensal
        - Score > 800 -> Aplica bônus de +50% sobre o limite base

    Retorna:
        float: Valor do limite aprovado formatado em 2 casas decimais.
    """
    if possui_restricao or renda < RENDA_MINIMA_APROVACAO:
        return 0.00

    limite_base = renda * PERCENTUAL_LIMITE_BASE

    if score > SCORE_MINIMO_BONUS:
        limite_base *= FATOR_BONUS_SCORE_ALTO

    return round(limite_base, 2)