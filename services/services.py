import random


def get_translation_optionals(
    cards: dict[str, str], word: str
) -> tuple[str, list[str]]:
    translation = cards[word]
    other_translation = [
        value for key, value in cards.items()
        if key != word and value != translation
    ]
    optional_translation = random.sample(
        other_translation,
        min(3, len(other_translation))
    )
    return translation, optional_translation
