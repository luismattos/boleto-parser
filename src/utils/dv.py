"""
Utilitários para cálculo de dígitos verificadores (DV) Módulo 10 e Módulo 11.
"""


def modulo_10(numero: str) -> int:
    """
    Calcula o dígito verificador usando Módulo 10.
    Args:
        numero: String numérica.
    Returns:
        Dígito verificador (0-9).
    """
    numero_invertido = numero[::-1]
    soma = 0
    for i, digito in enumerate(numero_invertido):
        peso = 2 if i % 2 == 0 else 1
        resultado = int(digito) * peso
        if resultado > 9:
            resultado = sum(int(d) for d in str(resultado))
        soma += resultado
    dv = 10 - (soma % 10)
    if dv == 10:
        dv = 0
    return dv


def modulo_11(numero: str) -> int:
    """
    Calcula o dígito verificador usando Módulo 11.
    Args:
        numero: String numérica.
    Returns:
        Dígito verificador (0-9 ou 1).
    """
    numero_invertido = numero[::-1]
    soma = 0
    for i, digito in enumerate(numero_invertido):
        peso = (i % 8) + 2  # Pesos de 2 a 9 (cíclicos)
        resultado = int(digito) * peso
        soma += resultado
    resto = soma % 11
    if resto == 0:
        dv = 1
    elif resto == 1:
        dv = 0
    else:
        dv = 11 - resto
    return dv
