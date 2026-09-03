from dataclasses import dataclass
from enum import Enum
from typing import List


class TipoTransacao(str, Enum):
    CREDITO = "CREDITO"
    DEBITO = "DEBITO"


class StatusTransacao(str, Enum):
    CONCLUIDO = "CONCLUIDO"
    ESTORNADO = "ESTORNADO"


class SaldoInsuficienteError(Exception):
    """Lançada quando uma tentativa de saque excede o saldo disponível."""
    pass


class TransacaoInvalidaError(Exception):
    """Lançada quando uma transação a ser estornada não existe ou já foi estornada."""
    pass


@dataclass
class Transacao:
    id: str
    valor: float
    tipo: TipoTransacao
    status: StatusTransacao


class LedgerContaCorrente:
    def __init__(self):
        pass

    def depositar(self, valor: float) -> Transacao:
        pass

    def sacar(self, valor: float) -> Transacao:
        pass

    def estornar(self, transacao_id: str) -> Transacao:
        pass

    def obter_saldo(self) -> float:
        pass

    def obter_historico(self) -> List[Transacao]:
        pass