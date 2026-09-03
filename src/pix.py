import re
import uuid


class ChavePixInvalidaError(Exception):
    """Exceção lançada quando uma chave Pix informada possui formato ou dados inválidos."""
    pass


def _validar_cpf(cpf: str) -> str:
    """Valida formato e dígitos verificadores de um CPF."""
    # Remove pontuações e mantém apenas números
    digitos = re.sub(r"\D", "", cpf)

    # Rejeita tamanho diferente de 11 ou sequências com todos os dígitos iguais
    if len(digitos) != 11 or digitos == digitos[0] * 11:
        raise ChavePixInvalidaError("CPF inválido")

    # 1º Dígito Verificador
    soma_1 = sum(int(digitos[i]) * (10 - i) for i in range(9))
    resto_1 = (soma_1 * 10) % 11
    digito_1 = 0 if resto_1 == 10 else resto_1

    # 2º Dígito Verificador
    soma_2 = sum(int(digitos[i]) * (11 - i) for i in range(10))
    resto_2 = (soma_2 * 10) % 11
    digito_2 = 0 if resto_2 == 10 else resto_2

    if int(digitos[9]) != digito_1 or int(digitos[10]) != digito_2:
        raise ChavePixInvalidaError("CPF inválido")

    return digitos


def _validar_email(email: str) -> str:
    """Valida o formato padrão de e-mail (usuario@dominio.com)."""
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(padrao, email):
        raise ChavePixInvalidaError("E-mail inválido")
    return email


def _validar_telefone(telefone: str) -> str:
    """Valida o formato de telefone com código do país (+55) e 11 dígitos."""
    if not re.match(r"^\+55\d{11}$", telefone):
        raise ChavePixInvalidaError("Telefone inválido")
    return telefone


def _validar_evp(chave: str) -> str:
    """Valida se a chave é um UUID versão 4 válido (36 caracteres)."""
    try:
        val = uuid.UUID(chave, version=4)
        if str(val) != chave.lower():
            raise ChavePixInvalidaError("Chave aleatória inválida")
        return chave
    except (ValueError, AttributeError):
        raise ChavePixInvalidaError("Chave aleatória inválida")


def validar_chave_pix(chave: str) -> tuple[str, str]:
    """
    Identifica o tipo da chave Pix e executa a validação correspondente.

    Retorna:
        tuple[str, str]: (tipo_da_chave, chave_normalizada)

    Lança:
        ChavePixInvalidaError: Caso o formato ou o conteúdo da chave seja inválido.
    """
    if not isinstance(chave, str):
        raise ChavePixInvalidaError("A chave deve ser uma string")

    chave_limpa = chave.strip()

    # 1. E-mail (possui @)
    if "@" in chave_limpa:
        return "EMAIL", _validar_email(chave_limpa)

    # 2. Telefone internacional (inicia com +)
    if chave_limpa.startswith("+"):
        return "TELEFONE", _validar_telefone(chave_limpa)

    # 3. Chave Aleatória EVP (UUID de 36 caracteres com hífens)
    if "-" in chave_limpa and len(chave_limpa) == 36:
        return "EVP", _validar_evp(chave_limpa)

    # 4. CPF (11 números ou máscara de CPF 000.000.000-00)
    apenas_numeros = re.sub(r"\D", "", chave_limpa)
    if len(apenas_numeros) == 11 and (chave_limpa.isdigit() or ("." in chave_limpa and "-" in chave_limpa)):
        return "CPF", _validar_cpf(chave_limpa)

    # 5. Se não se enquadrar em nenhum padrão conhecido
    raise ChavePixInvalidaError("Formato de chave Pix não reconhecido")