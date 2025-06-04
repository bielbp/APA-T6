"""
Biel Bernal Pratdesaba
"""

import re

def normalizaHoras(ficText, ficNorm):
    """
    Llegeix un fitxer de text, detecta expressions horàries vàlides i les substitueix pel format HH:MM.
    """

    # Patrons
    patron_hm_periodo = re.compile(
        r'\b(\d{1,2})h(?:\s+de la\s+(mañana|tarde|noche|madrugada))\b',
        re.IGNORECASE
    )
    patron_hm = re.compile(r'\b(\d{1,2})h(?:(\d{1,2})m)?\b')
    patron_colon = re.compile(r'\b(\d{1,2}):(\d{2})\b')
    patron_oral = re.compile(
        r'\b(\d{1,2})\s*(en punto|y cuarto|y media|menos cuarto)'
        r'(?:\s+de la\s+(mañana|tarde|noche|madrugada))?',
        re.IGNORECASE
    )
    patron_periodo = re.compile(
        r'\b(\d{1,2})\s*de la (mañana|tarde|noche|madrugada)\b|\b(\d{1,2})\s*del mediodía\b',
        re.IGNORECASE
    )

    with open(ficText, 'rt', encoding='utf-8') as f_in, open(ficNorm, 'wt', encoding='utf-8') as f_out:
        for linia in f_in:

            def substituir_hm_periodo(match):
                h = int(match.group(1))
                periode = match.group(2).lower()

                if not (1 <= h <= 12):
                    return match.group(0)

                if periode == 'mañana':
                    return f'{h % 12:02}:00'
                elif periode == 'tarde':
                    if 1 <= h <= 8:
                        return f'{(h + 12):02}:00'
                elif periode == 'noche':
                    if 8 <= h <= 11:
                        return f'{(h + 12):02}:00'
                    elif h == 12:
                        return '00:00'
                elif periode == 'madrugada':
                    if 1 <= h <= 6:
                        return f'{h:02}:00'

                return match.group(0)

            def substituir_hm(match):
                h, m = match.groups()
                h = int(h)
                m = int(m) if m is not None else 0
                return f'{h:02}:{m:02}' if 0 <= h <= 23 and 0 <= m <= 59 else match.group(0)

            def substituir_colon(match):
                h, m = int(match.group(1)), int(match.group(2))
                return f'{h:02}:{m:02}' if 0 <= h <= 23 and 0 <= m <= 59 else match.group(0)

            def substituir_oral(match):
                h = int(match.group(1))
                frase = match.group(2).lower()
                periode = match.group(3).lower() if match.group(3) else None

                if not (1 <= h <= 12):
                    return match.group(0)

                if frase == 'en punto':
                    m = 0
                elif frase == 'y cuarto':
                    m = 15
                elif frase == 'y media':
                    m = 30
                elif frase == 'menos cuarto':
                    h = (h - 1) if h > 1 else 12
                    m = 45
                else:
                    return match.group(0)

                if periode == 'tarde':
                    if 1 <= h <= 8:
                        h += 12
                elif periode == 'noche':
                    if 8 <= h <= 11:
                        h += 12
                    elif h == 12:
                        h = 0
                elif periode == 'mañana':
                    h = h % 12
                elif periode == 'madrugada':
                    if not (1 <= h <= 6):
                        return match.group(0)

                return f'{h:02}:{m:02}'

            def substituir_periodo(match):
                h1 = match.group(1)
                periode = match.group(2)
                h2 = match.group(3)

                if h2:  # del mediodía
                    h = int(h2)
                    if 1 <= h <= 2:
                        return f'{12 + (h % 12):02}:00'
                    return match.group(0)

                if not h1 or not periode:
                    return match.group(0)

                h = int(h1)
                periode = periode.lower()

                if not (1 <= h <= 12):
                    return match.group(0)

                if periode == 'mañana':
                    return f'{h % 12:02}:00'
                elif periode == 'tarde':
                    if 1 <= h <= 8:
                        return f'{(h + 12):02}:00'
                elif periode == 'noche':
                    if 8 <= h <= 11:
                        return f'{(h + 12):02}:00'
                    elif h == 12:
                        return '00:00'
                elif periode == 'madrugada':
                    if 1 <= h <= 6:
                        return f'{h:02}:00'

                return match.group(0)

            # Ordre de substitució
            linia = patron_hm_periodo.sub(substituir_hm_periodo, linia)
            linia = patron_hm.sub(substituir_hm, linia)
            linia = patron_colon.sub(substituir_colon, linia)
            linia = patron_oral.sub(substituir_oral, linia)
            linia = patron_periodo.sub(substituir_periodo, linia)

            f_out.write(linia)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)