import random


def get_translation_optionals(
    word_translations: dict[str, str], word: str
) -> tuple[str, list[str]]:
    translation = word_translations[word]
    other_translation = [
        value for key, value in word_translations.items()
        if key != word and value != translation
    ]
    optional_translation = random.sample(
        other_translation,
        min(3, len(other_translation))
    )
    return translation, optional_translation
