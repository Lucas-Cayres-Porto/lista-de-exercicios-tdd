import uuid
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
        self._transacoes: List[Transacao] = []

    def depositar(self, valor: float) -> Transacao:
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo")

        transacao = Transacao(
            id=str(uuid.uuid4()),
            valor=valor,
            tipo=TipoTransacao.CREDITO,
            status=StatusTransacao.CONCLUIDO,
        )
        self._transacoes.append(transacao)
        return transacao

    def sacar(self, valor: float) -> Transacao:
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo")

        if self.obter_saldo() < valor:
            raise SaldoInsuficienteError("Saldo insuficiente para realizar o saque")

        transacao = Transacao(
            id=str(uuid.uuid4()),
            valor=valor,
            tipo=TipoTransacao.DEBITO,
            status=StatusTransacao.CONCLUIDO,
        )
        self._transacoes.append(transacao)
        return transacao

    def estornar(self, transacao_id: str) -> Transacao:
        for transacao in self._transacoes:
            if transacao.id == transacao_id:
                if transacao.status != StatusTransacao.CONCLUIDO:
                    raise TransacaoInvalidaError("Transação já se encontra estornada")

                transacao.status = StatusTransacao.ESTORNADO
                return transacao

        raise TransacaoInvalidaError(f"Transação com ID {transacao_id} não encontrada")

    def obter_saldo(self) -> float:
        saldo = 0.0
        for t in self._transacoes:
            if t.status == StatusTransacao.CONCLUIDO:
                if t.tipo == TipoTransacao.CREDITO:
                    saldo += t.valor
                elif t.tipo == TipoTransacao.DEBITO:
                    saldo -= t.valor
        return round(saldo, 2)

    def obter_historico(self) -> List[Transacao]:
        return list(self._transacoes)