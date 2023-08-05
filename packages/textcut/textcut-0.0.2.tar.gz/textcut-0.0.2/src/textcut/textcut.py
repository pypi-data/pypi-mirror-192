import math
import re

from . import lang

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

    :param len_func: A function used to determine the length of the string,
        to accomodate for non-linear quantifications. Example:
        ``lambda x: sum([1 for c in x if c != " "])`` will count non-space
        characters only. Defaults to standard ``len``.
    :type len_func: Callable, optional
    """

    def __init__(self, language = lang.LANG_FR, width = 100, tolerance = 0.5,
                 trim = True, len_func = len):

        if width <= 0:
            raise ValueError(f"Invalid width value: {width}")

        self.language  = language
        self.width     = width
        self.tolerance = tolerance
        self.trim      = trim
        self.len_func  = len_func

        self.rules     = lang.CUT_RULES.get(self.language, lang.LANG_FR)


    def wrap(self, text):
        """ Wrap the text using the parameters defined in the constructor.

        :param text: The text to wrap
        :type text: str

        :return: One or more lines of no more than ``width``-character long.
        :rtype: Sequence[str]
        """

        probabilities = self.__compute_probabilities(text)
        lines = []
        while self.len_func(text) > self.width:
            max_i = 0
            max_p = 0
            i     = 1
            while self.len_func(text[:i]) < self.width + 1:
                x = i / self.width
                p = probabilities[i] * math.exp(-((x - 1) / self.tolerance) ** 2)
                if p >= max_p:
                    max_i = i
                    max_p = p

                i += 1

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
        """ Produces a string print-ready using ``\\n`` to collapse the lines.
        This method is a shortcut for ``"\\n".join(wrap(text))``.

        :param text: The text to wrap
        :type text: str

        :return: The wrapped lines glued together with a linefeed character (``\\n``).
        :rtype: str
        """

        return "\n".join(self.wrap(text))


    def __compute_probabilities(self, text):
        """ Compute the probability to cut before and after each character.
        Only the highest probability is stored.

        :param text: The text to compute
        :type text: str

        :return: Probabilities to cut the text at each position.
        :rtype: Sequence[float]
        """

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

        return probabilities


    def __findall_position(self, pattern, text, overlapping = True):
        """ Find all positions (beginning and end) of a pattern in text.

        :param pattern: The regex pattern to use with ``re.search``
        :type pattern: str
        :param text: The text to scan
        :type text: str
        :param overlapping: Whether to allow for overlapping positions or not;
            when set to ``False``, the returned positions are guaranteed to not
            overlap, defaults to ``True``
        :type overlapping: bool, optional

        :return: All the positions (beginning and end) in ``text`` where ``pattern``
            was found.
        :rtype: Sequence[Tuple[int, int]]
        """

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


