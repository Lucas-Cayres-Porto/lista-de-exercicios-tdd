import pytest
from src.ledger import (
    LedgerContaCorrente,
    TipoTransacao,
    StatusTransacao,
    SaldoInsuficienteError,
    TransacaoInvalidaError,
)


def test_conta_deve_iniciar_com_saldo_zero_e_historico_vazio():
    conta = LedgerContaCorrente()
    assert conta.obter_saldo() == 0.00
    assert conta.obter_historico() == []


def test_deve_realizar_deposito_com_sucesso():
    conta = LedgerContaCorrente()
    transacao = conta.depositar(1000.00)

    assert conta.obter_saldo() == 1000.00
    assert transacao.valor == 1000.00
    assert transacao.tipo == TipoTransacao.CREDITO
    assert transacao.status == StatusTransacao.CONCLUIDO
    assert len(conta.obter_historico()) == 1


def test_deve_realizar_saque_quando_houver_saldo():
    conta = LedgerContaCorrente()
    conta.depositar(1000.00)
    transacao_saque = conta.sacar(400.00)

    assert conta.obter_saldo() == 600.00
    assert transacao_saque.valor == 400.00
    assert transacao_saque.tipo == TipoTransacao.DEBITO
    assert transacao_saque.status == StatusTransacao.CONCLUIDO
    assert len(conta.obter_historico()) == 2


def test_deve_lancar_erro_ao_tentar_sacar_sem_saldo_suficiente():
    conta = LedgerContaCorrente()
    conta.depositar(200.00)

    with pytest.raises(SaldoInsuficienteError, match="Saldo insuficiente"):
        conta.sacar(500.00)

    # O saldo permanece inalterado e o saque não vai para o histórico
    assert conta.obter_saldo() == 200.00
    assert len(conta.obter_historico()) == 1


def test_deve_estornar_transacao_de_debito_e_recompor_saldo():
    conta = LedgerContaCorrente()
    conta.depositar(1000.00)
    saque = conta.sacar(300.00)
    assert conta.obter_saldo() == 700.00

    # Estorna o saque
    estorno = conta.estornar(saque.id)

    assert estorno.status == StatusTransacao.ESTORNADO
    assert conta.obter_saldo() == 1000.00  # Saldo recalculado imediatamente


def test_deve_estornar_transacao_de_credito_e_reduzir_saldo():
    conta = LedgerContaCorrente()
    deposito_1 = conta.depositar(500.00)
    conta.depositar(300.00)
    assert conta.obter_saldo() == 800.00

    # Estorna o primeiro depósito
    conta.estornar(deposito_1.id)
    assert conta.obter_saldo() == 300.00


def test_deve_lancar_erro_ao_tentar_estornar_transacao_ja_estornada():
    conta = LedgerContaCorrente()
    deposito = conta.depositar(500.00)
    conta.estornar(deposito.id)

    with pytest.raises(TransacaoInvalidaError):
        conta.estornar(deposito.id)


def test_deve_lancar_erro_ao_tentar_estornar_transacao_inexistente():
    conta = LedgerContaCorrente()
    with pytest.raises(TransacaoInvalidaError):
        conta.estornar("id-inexistente-123")


def test_fluxo_complexo_de_operacoes_e_estornos():
    """
    Desafio TDD: Testar sequência complexa de operações e múltiplos estornos
    """
    conta = LedgerContaCorrente()

    # 1. Depósitos
    t1 = conta.depositar(1000.00)  # Saldo: 1000.00
    t2 = conta.depositar(500.00)   # Saldo: 1500.00

    # 2. Saques
    t3 = conta.sacar(200.00)       # Saldo: 1300.00
    t4 = conta.sacar(300.00)       # Saldo: 1000.00

    assert conta.obter_saldo() == 1000.00

    # 3. Estorna um saque de 200.00
    conta.estornar(t3.id)          # Saldo volta para 1200.00
    assert conta.obter_saldo() == 1200.00

    # 4. Estorna um depósito de 500.00
    conta.estornar(t2.id)          # Saldo cai para 700.00
    assert conta.obter_saldo() == 700.00

    # 5. Novo saque de 700.00
    conta.sacar(700.00)            # Saldo: 0.00
    assert conta.obter_saldo() == 0.00

    # 6. Verifica integridade do histórico
    historico = conta.obter_historico()
    assert len(historico) == 5
    assert [t.status for t in historico] == [
        StatusTransacao.CONCLUIDO,
        StatusTransacao.ESTORNADO,
        StatusTransacao.ESTORNADO,
        StatusTransacao.CONCLUIDO,
        StatusTransacao.CONCLUIDO,
    ]