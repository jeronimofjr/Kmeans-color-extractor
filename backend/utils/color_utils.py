"""
Utilitários para manipulação de imagens.
"""

def rgb_to_hex(rgb: list) -> str:
    """
    Converte um array [R, G, B] (0-255) para uma string hexadecimal,
    ex: [30, 144, 255] -> "#1E90FF"
    """

    r, g, b = rgb
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    return f"#{r:02X}{g:02X}{b:02X}"