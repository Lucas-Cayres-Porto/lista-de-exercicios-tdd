from unittest.mock import MagicMock
import pytest
from src.conversor import ConversorMoeda, CotacaoAPI, ServicoCotacaoIndisponivelError


def test_deve_converter_moeda_com_sucesso_aplicando_spread_de_1_e_meio_porcento():
    # 1. ARRANGE (Preparação com Mock)
    # Simulamos a API externa retornando taxa de câmbio USD -> BRL = 5.00
    mock_api = MagicMock(spec=CotacaoAPI)
    mock_api.obter_taxa.return_value = 5.00

    conversor = ConversorMoeda(api_cotacao=mock_api)

    # 2. ACT (Ação)
    # Converter 100 USD:
    # 100 * 5.00 = 500.00
    # Spread de 1.5%: 500.00 * 1.015 = 507.50
    resultado = conversor.converter("USD", "BRL", 100.00)

    # 3. ASSERT (Verificação)
    assert resultado == pytest.approx(507.50, rel=1e-2)
    # Garante que a API externa foi chamada exatamente uma vez com os parâmetros corretos
    mock_api.obter_taxa.assert_called_once_with("USD", "BRL")


def test_deve_converter_outras_moedas_com_taxa_fracionada():
    mock_api = MagicMock(spec=CotacaoAPI)
    mock_api.obter_taxa.return_value = 6.20  # EUR -> BRL

    conversor = ConversorMoeda(api_cotacao=mock_api)

    # 50 * 6.20 = 310.00 -> Com 1.5% = 310.00 * 1.015 = 314.65
    resultado = conversor.converter("EUR", "BRL", 50.00)

    assert resultado == pytest.approx(314.65, rel=1e-2)
    mock_api.obter_taxa.assert_called_once_with("EUR", "BRL")


def test_deve_lancar_erro_quando_api_externa_estiver_fora_do_ar():
    # Simulamos uma queda de conexão (ConnectionError) na API externa
    mock_api = MagicMock(spec=CotacaoAPI)
    mock_api.obter_taxa.side_effect = ConnectionError("Connection refused by external server")

    conversor = ConversorMoeda(api_cotacao=mock_api)

    # O conversor deve capturar o erro de rede e relançar ServicoCotacaoIndisponivelError
    with pytest.raises(ServicoCotacaoIndisponivelError, match="Serviço de cotação temporariamente indisponível"):
        conversor.converter("USD", "BRL", 100.00)


def test_deve_lancar_erro_quando_api_externa_der_timeout():
    # Simulamos um Timeout na API externa
    mock_api = MagicMock(spec=CotacaoAPI)
    mock_api.obter_taxa.side_effect = TimeoutError("Request timed out")

    conversor = ConversorMoeda(api_cotacao=mock_api)

    with pytest.raises(ServicoCotacaoIndisponivelError):
        conversor.converter("USD", "BRL", 100.00)


def test_deve_lancar_erro_para_valor_negativo_ou_zero():
    mock_api = MagicMock(spec=CotacaoAPI)
    conversor = ConversorMoeda(api_cotacao=mock_api)

    with pytest.raises(ValueError, match="O valor para conversão deve ser positivo"):
        conversor.converter("USD", "BRL", -50.00)

    with pytest.raises(ValueError, match="O valor para conversão deve ser positivo"):
        conversor.converter("USD", "BRL", 0.00)

    # Garante que nem chamou a API externa se o valor for inválido
    mock_api.obter_taxa.assert_not_called()