import pytest
from src.credito import avaliar_limite_credito


@pytest.mark.parametrize(
    "renda, possui_restricao, score, limite_esperado",
    [
        # Regra 1: Renda abaixo do mínimo
        (1000.00, False, 900, 0.00),
        (1499.99, False, 850, 0.00),

        # Regra 2: Restrição cadastral (nome sujo)
        (5000.00, True, 950, 0.00),
        (1000.00, True, 500, 0.00),
        (1500.00, True, 850, 0.00),

        # Regra 3: Aprovado sem bônus (Score <= 800)
        (1500.00, False, 700, 450.00),
        (1500.00, False, 800, 450.00),
        (3000.00, False, 600, 900.00),

        # Regra 4: Aprovado com bônus de score alto (Score > 800)
        (1500.00, False, 801, 675.00),
        (3000.00, False, 850, 1350.00),
        (10000.00, False, 1000, 4500.00),
    ],
    ids=[
        "renda_abaixo_minimo_com_score_alto",
        "renda_borda_inferior",
        "restricao_com_renda_alta_e_score_alto",
        "restricao_com_renda_baixa",
        "restricao_com_renda_minima",
        "renda_minima_score_comum",
        "renda_minima_score_borda_800",
        "renda_media_score_comum",
        "renda_minima_score_bonus_801",
        "renda_media_score_bonus_850",
        "renda_alta_score_maximo_1000",
    ],
)
def test_avaliar_limite_credito(renda, possui_restricao, score, limite_esperado):
    limite_calculado = avaliar_limite_credito(renda, possui_restricao, score)
    assert limite_calculado == pytest.approx(limite_esperado, rel=1e-2)