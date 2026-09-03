# 💳 Lista de Exercícios Práticos de TDD - Domínio Fintech

> **Engenharia e Qualidade de Software**  
> **Integrantes:**  
> • **Lucas Cayres Porto** — Nº 16  
> • **Carlos Eduardo Rodrigues Do Amaral** — Nº 4  
> **Turma:** 2º E  

---

## 📖 Visão Geral

Repositório dedicado à implementação de 4 casos de uso práticos voltados para o domínio de **Fintech (mercado financeiro)**, aplicando rigorosamente a metodologia **TDD (Test-Driven Development)** utilizando **Python** e **Pytest**.

Cada funcionalidade foi desenvolvida em branch própria, seguindo o ciclo **Red ➔ Green ➔ Refactor** e integrada à branch principal através de Pull Requests.

---

## 🔄 O Ciclo TDD Aplicado

```text
    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    ▼                                                         │
1. 🔴 RED           ➔   2. 🟢 GREEN        ➔    3. 🔵 REFACTOR ┘
(Escrever os testes     (Implementação mínima    (Melhorar design e
 que falham primeiro)    para os testes passarem) tipagem mantendo verde)
```

---

## 📂 Casos de Uso, Pull Requests e Resultados

### 1️⃣ Exercício 1: Validador de Chave Pix
* **Módulo:** `src/pix.py` | **Testes:** `tests/test_pix.py`
* **Pull Request:** [🔗 PR #1 - Feat/validador de chave pix](https://github.com/Lucas-Cayres-Porto/lista-de-exercicios-tdd/pull/1)
* **Regras de Negócio:**
  * **CPF:** 11 dígitos numéricos com validação matemática dos 2 dígitos verificadores e rejeição de sequências repetidas.
  * **E-mail:** Formato válido (`usuario@dominio.com`).
  * **Telefone:** Código internacional `+55` + DDD + 9 dígitos (11 dígitos numéricos).
  * **Chave Aleatória (EVP):** UUID versão 4 válido de 36 caracteres.
  * **Exceção Customizada:** Disparo de `ChavePixInvalidaError` para formatos inválidos.
* **Resultado da Suíte de Testes:**
  * 🔴 **RED:** 13 testes falhando (`13 failed in 1.27s`)
  * 🟢 **GREEN:** 13 testes passando (`13 passed in 0.45s`)
  * 🔵 **REFACTOR:** 13 testes passando (`13 passed in 1.35s`)

---

### 2️⃣ Exercício 2: Motor de Análise de Risco de Crédito (Score Interno)
* **Módulo:** `src/credito.py` | **Testes:** `tests/test_credito.py`
* **Pull Request:** [🔗 PR #2 - Feat/motor de analise de risco de credito](https://github.com/Lucas-Cayres-Porto/lista-de-exercicios-tdd/pull/2)
* **Regras de Negócio:**
  * **Regra 1:** Renda mensal < R$ 1.500,00 $\to$ Limite: `R$ 0,00` (Crédito negado).
  * **Regra 2:** Restrição no CPF (nome sujo) $\to$ Limite: `R$ 0,00` independente de renda ou score.
  * **Regra 3:** Renda $\ge$ R$ 1.500,00 sem restrições $\to$ Limite inicial base = 30% da renda.
  * **Regra 4:** Score externo > 800 $\to$ Bônus de +50% sobre o limite inicial base.
* **Desafio TDD:** Utilização de `@pytest.mark.parametrize` com IDs descritivos para cobrir a matriz de combinações.
* **Resultado da Suíte de Testes:**
  * 🔴 **RED:** 11 testes parametrizados falhando (`11 failed in 3.30s`)
  * 🟢 **GREEN:** 11 testes passando (`11 passed in 0.19s`)
  * 🔵 **REFACTOR:** 11 testes passando (`11 passed in 0.20s`)

---

### 3️⃣ Exercício 3: Processador de Extrato Extornável (Ledger de Transações)
* **Módulo:** `src/ledger.py` | **Testes:** `tests/test_ledger.py`
* **Pull Request:** [🔗 PR #3 - Feat/processador de extrato extornavel](https://github.com/Lucas-Cayres-Porto/lista-de-exercicios-tdd/pull/3)
* **Regras de Negócio:**
  * **Transações:** Entidade com `id`, `valor`, `tipo` (`CREDITO`/`DEBITO`) e `status` (`CONCLUIDO`/`ESTORNADO`).
  * **Saldo Disponível:** $\sum \text{Créditos CONCLUIDO} - \sum \text{Débitos CONCLUIDO}$.
  * **Saque Bloqueado:** Dispara `SaldoInsuficienteError` caso o saldo não seja suficiente.
  * **Estorno Imediato:** Estorno permitido apenas para transações `CONCLUIDO`, mudando o status para `ESTORNADO` com recálculo instantâneo de saldo. Lança `TransacaoInvalidaError` caso contrário.
* **Resultado da Suíte de Testes:**
  * 🔴 **RED:** 9 testes falhando (`9 failed in 1.33s`)
  * 🟢 **GREEN:** 9 testes passando (`9 passed in 0.17s`)
  * 🔵 **REFACTOR:** 9 testes passando (`9 passed in 0.17s`)

---

### 4️⃣ Exercício 4: Conversor de Moedas em Tempo Real com Mock de API
* **Módulo:** `src/conversor.py` | **Testes:** `tests/test_conversor.py`
* **Pull Request:** [🔗 PR #4 - Feat/conversor de moedas em tempo real](https://github.com/Lucas-Cayres-Porto/lista-de-exercicios-tdd/pull/4)
* **Regras de Negócio:**
  * **Conversão:** Converte moeda de origem para destino consumindo taxa da `CotacaoAPI`.
  * **Taxa de Spread:** Aplica taxa de serviço fixa de 1.5% sobre o valor convertido final.
  * **Resiliência e Quedas de Rede:** Captura falhas/timeouts da API externa e lança `ServicoCotacaoIndisponivelError`.
* **Desafio TDD:** Utilização de Mocks (`unittest.mock.MagicMock`) para isolar completamente chamadas de rede externas e simular múltiplos cenários e exceções.
* **Resultado da Suíte de Testes:**
  * 🔴 **RED:** 5 testes falhando (`5 failed in 0.24s`)
  * 🟢 **GREEN:** 5 testes passando (`5 passed in 0.18s`)
  * 🔵 **REFACTOR:** 5 testes passando (`5 passed in 0.14s`)

---

## 📊 Matriz Geral de Cobertura e Testes

| # | Exercício | Arquivo de Código | Arquivo de Teste | Qtd. Testes | Status |
| :-: | :--- | :--- | :--- | :-: | :-: |
| **1** | Validador de Chave Pix | `src/pix.py` | `tests/test_pix.py` | 13 | 🟢 100% Aprovado |
| **2** | Motor de Risco de Crédito | `src/credito.py` | `tests/test_credito.py` | 11 | 🟢 100% Aprovado |
| **3** | Ledger de Transações | `src/ledger.py` | `tests/test_ledger.py` | 9 | 🟢 100% Aprovado |
| **4** | Conversor com Mock de API | `src/conversor.py` | `tests/test_conversor.py` | 5 | 🟢 100% Aprovado |
| **TOTAL** | — | — | — | **38** | 🟢 **38 passed** |

---

## 🚀 Como Executar os Testes

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/Lucas-Cayres-Porto/lista-de-exercicios-tdd.git
   cd lista-de-exercicios-tdd
   ```

2. **Instalar as dependências de teste:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar toda a suíte de testes:**
   ```bash
   pytest -v
   ```

4. **Executar um exercício individual:**
   ```bash
   pytest tests/test_pix.py -v
   pytest tests/test_credito.py -v
   pytest tests/test_ledger.py -v
   pytest tests/test_conversor.py -v
   ```
