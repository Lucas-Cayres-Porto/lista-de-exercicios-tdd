import pytest
from src.pix import validar_chave_pix, ChavePixInvalidaError


# 1. TESTES PARA CPF

# CPF válido
def test_cpf_valido():
    tipo, chave = validar_chave_pix("52998224725")
    assert tipo == "CPF"
    assert chave == "52998224725"

# CPF válido com formatacão
def test_cpf_valido_com_formatacao():
    tipo, chave = validar_chave_pix("529.982.247-25")
    assert tipo == "CPF"
    assert chave == "52998224725"

# CPF inválido com verificadores errados
def test_cpf_com_digitos_verificadores_invalidos():
    with pytest.raises(ChavePixInvalidaError, match="CPF inválido"):
        validar_chave_pix("12345678900")

# CPF inválido com digitos todos iguais
def test_cpf_com_todos_digitos_iguais():
    with pytest.raises(ChavePixInvalidaError, match="CPF inválido"):
        validar_chave_pix("11111111111")


# 2. TESTES PARA E-MAIL

# Email
def test_email_valido():
    tipo, chave = validar_chave_pix("usuario@dominio.com")
    assert tipo == "EMAIL"
    assert chave == "usuario@dominio.com"


def test_email_sem_arroba_deve_lancar_erro():
    with pytest.raises(ChavePixInvalidaError):
        validar_chave_pix("usuariodominio.com")


def test_email_sem_dominio_deve_lancar_erro():
    with pytest.raises(ChavePixInvalidaError):
        validar_chave_pix("usuario@")


# 3. TESTES PARA TELEFONE

# Telefone válido
def test_telefone_valido():
    tipo, chave = validar_chave_pix("+5511999998888")
    assert tipo == "TELEFONE"
    assert chave == "+5511999998888"

# telefone invalido por estar sem código
def test_telefone_sem_codigo_pais_deve_lancar_erro():
    with pytest.raises(ChavePixInvalidaError, match="Telefone inválido"):
        validar_chave_pix("11999998888")


# telefone invalido com tamanho menor
def test_telefone_com_tamanho_incorreto_deve_lancar_erro():
    with pytest.raises(ChavePixInvalidaError, match="Telefone inválido"):
        validar_chave_pix("+55119999888")


# 4. TESTES PARA CHAVE ALEATÓRIA (EVP - UUIDv4)

# uuid validp
def test_chave_aleatoria_evp_uuidv4_valida():
    uuid_valido = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    tipo, chave = validar_chave_pix(uuid_valido)
    assert tipo == "EVP"
    assert chave == uuid_valido


# uuid com padrão inválido
def test_chave_aleatoria_com_uuid_versao_diferente_de_4_deve_lancar_erro():
    uuid_v1 = "a0eebc99-9c0b-1ef8-bb6d-6bb9bd380a11"
    with pytest.raises(ChavePixInvalidaError):
        validar_chave_pix(uuid_v1)


# 5. TESTES PARA FORMATO DESCONHECIDO

# teste com formato aleatorio 
def test_formato_desconhecido_deve_lancar_erro():
    with pytest.raises(ChavePixInvalidaError):
        validar_chave_pix("texto_invalido_sem_nenhum_formato")