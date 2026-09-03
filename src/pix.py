import re
import uuid
from enum import Enum


class TipoChavePix(str, Enum):
    """Enumeração com os tipos de chaves Pix suportados."""
    CPF = "CPF"
    EMAIL = "EMAIL"
    TELEFONE = "TELEFONE"
    EVP = "EVP"


class ChavePixInvalidaError(Exception):
    """Exceção lançada quando uma chave Pix informada possui formato ou conteúdo inválido."""
    pass


# Padrões compilados para melhor performance
PADRAO_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
PADRAO_TELEFONE = re.compile(r"^\+55\d{11}$")


def _calcular_digito_cpf(digitos: str, peso_inicial: int) -> int:
    """Calcula um dígito verificador do CPF através da soma ponderada."""
    soma = sum(int(digito) * (peso_inicial - i) for i, digito in enumerate(digitos))
    resto = (soma * 10) % 11
    return 0 if resto == 10 else resto


def _validar_cpf(cpf: str) -> str:
    """Valida o formato e os dois dígitos verificadores do CPF."""
    digitos = re.sub(r"\D", "", cpf)

    if len(digitos) != 11 or digitos == digitos[0] * 11:
        raise ChavePixInvalidaError("CPF inválido")

    d1 = _calcular_digito_cpf(digitos[:9], 10)
    d2 = _calcular_digito_cpf(digitos[:10], 11)

    if int(digitos[9]) != d1 or int(digitos[10]) != d2:
        raise ChavePixInvalidaError("CPF inválido")

    return digitos


def _validar_email(email: str) -> str:
    """Valida o formato padrão de e-mail (usuario@dominio.com)."""
    if not PADRAO_EMAIL.match(email):
        raise ChavePixInvalidaError("E-mail inválido")
    return email


def _validar_telefone(telefone: str) -> str:
    """Valida o formato de telefone internacional (+55 + DDD + 9 dígitos)."""
    if not PADRAO_TELEFONE.match(telefone):
        raise ChavePixInvalidaError("Telefone inválido")
    return telefone


def _validar_evp(chave: str) -> str:
    """Valida se a chave aleatória é um UUID versão 4 de 36 caracteres."""
    try:
        val = uuid.UUID(chave, version=4)
        if str(val) != chave.lower():
            raise ChavePixInvalidaError("Chave aleatória inválida")
        return chave
    except (ValueError, AttributeError):
        raise ChavePixInvalidaError("Chave aleatória inválida")


def validar_chave_pix(chave: str) -> tuple[TipoChavePix, str]:
    """
    Identifica o tipo da chave Pix e executa a validação correspondente.

    Retorna:
        tuple[TipoChavePix, str]: (tipo_da_chave, chave_normalizada)

    Lança:
        ChavePixInvalidaError: Caso o formato ou o conteúdo da chave seja inválido.
    """
    if not isinstance(chave, str):
        raise ChavePixInvalidaError("A chave deve ser uma string")

    chave_limpa = chave.strip()

    # 1. E-mail (contém @)
    if "@" in chave_limpa:
        return TipoChavePix.EMAIL, _validar_email(chave_limpa)

    # 2. Telefone internacional (inicia com +)
    if chave_limpa.startswith("+"):
        return TipoChavePix.TELEFONE, _validar_telefone(chave_limpa)

    # 3. Chave Aleatória EVP (UUID de 36 caracteres com hífens)
    if len(chave_limpa) == 36 and chave_limpa.count("-") == 4:
        return TipoChavePix.EVP, _validar_evp(chave_limpa)

    # 4. CPF (11 números ou máscara 000.000.000-00)
    apenas_numeros = re.sub(r"\D", "", chave_limpa)
    if len(apenas_numeros) == 11 and (chave_limpa.isdigit() or ("." in chave_limpa and "-" in chave_limpa)):
        return TipoChavePix.CPF, _validar_cpf(chave_limpa)

    # 5. Formato não reconhecido
    raise ChavePixInvalidaError("Formato de chave Pix não reconhecido")
