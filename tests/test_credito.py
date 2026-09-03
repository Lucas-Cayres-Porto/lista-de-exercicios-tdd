import pytest
from src.credito import avaliar_limite_credito


@pytest.mark.parametrize(
    "renda, possui_restricao, score, limite_esperado",
    [
        # -------------------------------------------------------------
        # Regra 1: Renda < R$ 1.500,00 -> Crédito negado (R$ 0,00)
        # -------------------------------------------------------------
        (1000.00, False, 900, 0.00),
        (1499.99, False, 850, 0.00),

        # -------------------------------------------------------------
        # Regra 2: Restrição no CPF (nome sujo) -> Limite R$ 0,00
        # -------------------------------------------------------------
        (5000.00, True, 950, 0.00),
        (1000.00, True, 500, 0.00),
        (1500.00, True, 850, 0.00),

        # -------------------------------------------------------------
        # Regra 3: Renda >= R$ 1.500,00 sem restrição (30% da renda base)
        # -------------------------------------------------------------
        (1500.00, False, 700, 450.00),
        (1500.00, False, 800, 450.00),  # Score 800 exato (não recebe bônus)
        (3000.00, False, 600, 900.00),

        # -------------------------------------------------------------
        # Regra 4: Score > 800 (+50% de bônus sobre o limite base)
        # -------------------------------------------------------------
        (1500.00, False, 801, 675.00),    # 450.00 * 1.50 = 675.00
        (3000.00, False, 850, 1350.00),   # 900.00 * 1.50 = 1350.00
        (10000.00, False, 1000, 4500.00), # 3000.00 * 1.50 = 4500.00
    ],
)
def test_avaliar_limite_credito(renda, possui_restricao, score, limite_esperado):
    limite_calculado = avaliar_limite_credito(renda, possui_restricao, score)
    assert limite_calculado == pytest.approx(limite_esperado, rel=1e-2)