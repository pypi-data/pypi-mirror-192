import math
import re

class TextCut:
    """ Wrap a text based on more advanced probabilities,
    depending on the context of the text. The probabilities
    depends on the language.

    :param language: The text language, defaults to french (fr)
    :type language: str, optional

    :param width: The maximal width of each line, defaults to 100
    :type width: int, optional

    :param tolerance: How short the wrapper is tolerant to shorter
        string than requested. High value (>5) basically means the
        wrapper does not care about the length of the results, but
        will look for the best cutting position. For value around
        0.5 to 1.0, the wrapper will prefer longer lines (closer to
        the requested width), but may occasionnaly choose a shorter
        line, if it gives a good compromise. Low value (<0.1) will
        always prefer long lines, even if it means cutting between
        words instead of paragraph, or even within words. Defaults
        to 0.5
    :type tolerance: float, optional

    :param trim: Trim white spaces for each line, defaults to True
    :type trim: bool, optional
    """

    LANG_FR = 'fr'

    CUT_RULES = {'fr': {'after':   {'\n\n'   : 1,   '\n'   : 0.95, r'\.\s' : 0.9, r'!\s' : 0.9,
                                    r'\?\s'  : 0.9, r';\s' : 0.85, r',\s'  : 0.8, r':\s' : 0.85,
                                    r'\)'    : 0.6, r'\]'  : 0.6,  r'\}'   : 0.6, r'»'   : 0.6,
                                    r'\.\.\.': 0.6, r'-'   : 0.3,  r'\s'   : 0.2},
                        'before':  {r'\('    : 0.6, r'\['  : 0.6,  r'\{'   : 0.6, r'«'   : 0.6},
                        'default': 0.01}}


    def __init__(self, language = 'fr', width = 100, tolerance = 0.5, trim = True):
        self.language  = language
        self.width     = width
        self.tolerance = tolerance
        self.trim      = trim

        self.rules     = TextCut.CUT_RULES.get(self.language, 'fr')


    def wrap(self, text):
        probabilities = [self.rules.get('default', 0)] * (len(text) + 1)
        after  = self.rules.get('after',  {})
        before = self.rules.get('before', {})

        for seq, proba in after.items():
            for cut in self.__findall_position(seq, text):
                position = cut[1]
                probabilities[position] = max(probabilities[position], proba)

        for seq, proba in before.items():
            for cut in self.__findall_position(seq, text):
                position = cut[0]
                probabilities[position] = max(probabilities[position], proba)

        lines = []
        while len(text) > self.width:
            max_i = 0
            max_p = 0
            for i in range(1, self.width+1):
                x = i / (self.width + 1)
                p = probabilities[i] * math.exp(-((x - 1) / self.tolerance) ** 2)
                if p >= max_p:
                    max_i = i
                    max_p = p

            lines         += [text[:max_i]]
            text           = text[max_i:]
            probabilities  = probabilities[max_i:]

            if self.trim:
                lines[-1] = lines[-1].strip()


        lines += [text]
        if self.trim:
            lines[-1] = lines[-1].strip()

        return lines


    def fill(self, text):
        return "\n".join(self.wrap(text))


    def __findall_position(self, pattern, text, overlapping = True):
        cursor = 0
        while True:
            result = re.search(pattern, text[cursor:], re.MULTILINE)
            if result is None:
                break

            yield (result.start() + cursor, result.end() + cursor)
            if overlapping:
                cursor += result.start() + 1
            else:
                cursor += result.end()


