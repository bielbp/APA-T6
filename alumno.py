"""
Biel Bernal Pratdesaba
"""
import re

class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'

def leeAlumnos(ficAlum):
    """
    Llegeix un fitxer de text que conté les dades dels alumnes i retorna un diccionari amb objectes Alumno.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcell de Lara 4.9
    68      David Garcia Fuster     7.0
    """
    dicAlumnes = {}
    patro = re.compile(r"^(\d+)\s+(.*?)\s+([\d.\s]+)$")

    with open(ficAlum, "rt") as fpAlumnes:
        for alumne in fpAlumnes:
            alumne = alumne.strip()
            aux = patro.match(alumne)
            if aux:
                numero = aux.group(1)
                noms = aux.group(2).strip()
                notes = re.findall(r"\d+(?:\.\d+)?", aux.group(3))                    
                info = Alumno(noms, int(numero), list(map(float, notes)))
                dicAlumnes[noms] = info
    return dicAlumnes


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)