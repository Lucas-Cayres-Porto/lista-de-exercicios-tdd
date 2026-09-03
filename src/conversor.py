class ServicoCotacaoIndisponivelError(Exception):
    """Exceção lançada quando a API externa de cotação está indisponível ou falha."""
    pass


class CotacaoAPI:
    """Interface / Conector que se comunica com o serviço de câmbio externo."""

    def obter_taxa(self, origem: str, destino: str) -> float:
        """Obtém a taxa de câmbio entre as duas moedas."""
        raise NotImplementedError("Método real deve ser consumido via HTTP.")


class ConversorMoeda:
    """Serviço de conversão monetária que aplica taxa de spread de 1.5%."""

    TAXA_SPREAD = 0.015  # 1.5% de taxa de serviço fixa

    def __init__(self, api_cotacao: CotacaoAPI = None):
        # Injeção de dependência: se não receber uma API mockada, usa a classe padrão
        self.api_cotacao = api_cotacao or CotacaoAPI()

    def converter(self, origem: str, destino: str, valor: float) -> float:
        """
        Converte um valor monetário de uma moeda para outra aplicando o spread de 1.5%.
        """
        if valor <= 0:
            raise ValueError("O valor para conversão deve ser positivo")

        try:
            taxa = self.api_cotacao.obter_taxa(origem, destino)
        except Exception as erro:
            raise ServicoCotacaoIndisponivelError(
                f"Serviço de cotação temporariamente indisponível: {erro}"
            ) from erro

        # Aplica a taxa de conversão com spread de 1.5%
        valor_convertido = (valor * taxa) * (1 + self.TAXA_SPREAD)
        return round(valor_convertido, 2)