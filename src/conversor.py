class ServicoCotacaoIndisponivelError(Exception):
    """Exceção lançada quando a API externa de cotação está indisponível ou falha."""
    pass


class CotacaoAPI:
    """Interface / Conector que se comunica com a API externa de câmbio."""
    def obter_taxa(self, origem: str, destino: str) -> float:
        raise NotImplementedError("Método deve ser consumido via rede ou mockado em testes.")


class ConversorMoeda:
    """Serviço responsável por realizar a conversão monetária com aplicação de spread."""
    def __init__(self, api_cotacao: CotacaoAPI = None):
        pass

    def converter(self, origem: str, destino: str, valor: float) -> float:
        pass