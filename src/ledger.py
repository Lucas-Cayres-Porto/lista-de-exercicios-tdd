import uuid
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class TipoTransacao(str, Enum):
    """Tipos de movimentação financeira no ledger."""
    CREDITO = "CREDITO"
    DEBITO = "DEBITO"


class StatusTransacao(str, Enum):
    """Estados possíveis de uma transação."""
    CONCLUIDO = "CONCLUIDO"
    ESTORNADO = "ESTORNADO"


class SaldoInsuficienteError(Exception):
    """Lançada quando uma tentativa de saque excede o saldo disponível."""
    pass


class TransacaoInvalidaError(Exception):
    """Lançada quando a transação a ser estornada não existe ou já foi estornada."""
    pass


@dataclass
class Transacao:
    """Entidade que representa uma movimentação no livro-razão."""
    id: str
    valor: float
    tipo: TipoTransacao
    status: StatusTransacao

    def estornar(self) -> None:
        """Altera o status da transação para ESTORNADO."""
        if self.status != StatusTransacao.CONCLUIDO:
            raise TransacaoInvalidaError("Apenas transações com status CONCLUIDO podem ser estornadas")
        self.status = StatusTransacao.ESTORNADO


class LedgerContaCorrente:
    """Livro-razão responsável pela gestão de saldo, operações e estornos."""

    def __init__(self):
        self._transacoes: List[Transacao] = []

    def _criar_transacao(self, valor: float, tipo: TipoTransacao) -> Transacao:
        """Cria e registra uma nova transação no histórico."""
        if valor <= 0:
            raise ValueError(f"O valor de {tipo.value.lower()} deve ser estritamente positivo")

        transacao = Transacao(
            id=str(uuid.uuid4()),
            valor=valor,
            tipo=tipo,
            status=StatusTransacao.CONCLUIDO,
        )
        self._transacoes.append(transacao)
        return transacao

    def _buscar_transacao(self, transacao_id: str) -> Transacao:
        """Busca uma transação pelo ID ou levanta TransacaoInvalidaError."""
        for t in self._transacoes:
            if t.id == transacao_id:
                return t
        raise TransacaoInvalidaError(f"Transação com ID '{transacao_id}' não encontrada")

    def depositar(self, valor: float) -> Transacao:
        """Realiza um depósito (crédito) na conta corrente."""
        return self._criar_transacao(valor, TipoTransacao.CREDITO)

    def sacar(self, valor: float) -> Transacao:
        """Realiza um saque (débito) caso haja saldo disponível."""
        if self.obter_saldo() < valor:
            raise SaldoInsuficienteError("Saldo insuficiente para realizar o saque")
        return self._criar_transacao(valor, TipoTransacao.DEBITO)

    def estornar(self, transacao_id: str) -> Transacao:
        """Aplica o estorno a uma transação concluída e recalcula o saldo imediatamente."""
        transacao = self._buscar_transacao(transacao_id)
        transacao.estornar()
        return transacao

    def obter_saldo(self) -> float:
        """Calcula o saldo disponível: soma(créditos concluídos) - soma(débitos concluídos)."""
        creditos = sum(
            t.valor
            for t in self._transacoes
            if t.tipo == TipoTransacao.CREDITO and t.status == StatusTransacao.CONCLUIDO
        )
        debitos = sum(
            t.valor
            for t in self._transacoes
            if t.tipo == TipoTransacao.DEBITO and t.status == StatusTransacao.CONCLUIDO
        )
        return round(creditos - debitos, 2)

    def obter_historico(self) -> List[Transacao]:
        """Retorna uma cópia do histórico de todas as transações."""
        return list(self._transacoes)