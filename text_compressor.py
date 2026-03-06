"""
Compress slide text for readability.
Strips filler phrases and hard-limits line length.
"""


class TextCompressor:

    FILLER = [
        "in order to", "it is important to note that",
        "it should be noted that", "as a matter of fact",
    ]

    def compress(self, content: list, max_words: int = 14) -> list:
        """
        Trim each bullet to max_words words and strip common filler phrases.
        max_words raised from 12 → 14 so context is not lost mid-sentence.
        """
        result = []
        for point in content:
            # strip filler
            lower = point.lower()
            for phrase in self.FILLER:
                lower = lower.replace(phrase, "")
            # restore capitalisation from original where possible
            cleaned = point
            for phrase in self.FILLER:
                cleaned = cleaned.replace(phrase, "").replace(phrase.capitalize(), "")

            cleaned = " ".join(cleaned.split())   # normalise whitespace

            words = cleaned.split()
            if len(words) > max_words:
                cleaned = " ".join(words[:max_words]) + "..."

            if cleaned:
                result.append(cleaned)

        return result