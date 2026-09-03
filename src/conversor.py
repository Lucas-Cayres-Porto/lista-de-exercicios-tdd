from typing import Optional


class ServicoCotacaoIndisponivelError(Exception):
    """Exceção lançada quando a API externa de cotação está indisponível ou falha."""
    pass


class CotacaoAPI:
    """Interface / Conector com o provedor de cotação de câmbio externo."""

    def obter_taxa(self, origem: str, destino: str) -> float:
        """Obtém a taxa de câmbio entre as moedas de origem e destino."""
        raise NotImplementedError("Método deve ser consumido via HTTP real ou mockado.")


class ConversorMoeda:
    """Serviço responsável por realizar a conversão monetária com aplicação de taxa de spread."""

    PERCENTUAL_SPREAD_FIXO: float = 0.015  # Taxa de serviço de 1.5%

    def __init__(self, api_cotacao: Optional[CotacaoAPI] = None):
        self._api_cotacao = api_cotacao or CotacaoAPI()

    def _aplicar_spread(self, valor_bruto: float) -> float:
        """Aplica a taxa fixa de spread de 1.5% sobre o valor convertido bruto."""
        valor_com_spread = valor_bruto * (1.0 + self.PERCENTUAL_SPREAD_FIXO)
        return round(valor_com_spread, 2)

    def converter(self, origem: str, destino: str, valor: float) -> float:
        """
        Converte um montante da moeda de origem para a moeda de destino.

        Args:
            origem (str): Código da moeda de origem (ex: 'USD').
            destino (str): Código da moeda de destino (ex: 'BRL').
            valor (float): Montante a ser convertido (deve ser > 0).

        Returns:
            float: Valor final convertido acrescido da taxa de serviço.

        Raises:
            ValueError: Se o valor for menor ou igual a zero.
            ServicoCotacaoIndisponivelError: Se a API de cotação falhar.
        """
        if valor <= 0:
            raise ValueError("O valor para conversão deve ser positivo")

        moeda_origem = origem.strip().upper()
        moeda_destino = destino.strip().upper()

        try:
            taxa = self._api_cotacao.obter_taxa(moeda_origem, moeda_destino)
        except Exception as erro:
            raise ServicoCotacaoIndisponivelError(
                f"Serviço de cotação temporariamente indisponível: {erro}"
            ) from erro

        valor_bruto = valor * taxa
        return self._aplicar_spread(valor_bruto)