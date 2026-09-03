class ChavePixInvalidaError(Exception):
    """Exceção lançada quando uma chave Pix informada possui formato inválido."""
    pass


def validar_chave_pix(chave: str) -> tuple[str, str]:
    """
    Identifica e valida o tipo de chave Pix (CPF, E-mail, Telefone ou EVP).
    Retorna uma tupla (tipo, chave_normalizada) ou lança ChavePixInvalidaError.
    """
    pass