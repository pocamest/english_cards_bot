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


DEFAULT_WORDS = [
    {"word": "белый", "translation": "white"},
    {"word": "чёрный", "translation": "black"},
    {"word": "красный", "translation": "red"},
    {"word": "синий", "translation": "blue"},
    {"word": "зелёный", "translation": "green"},
    {"word": "жёлтый", "translation": "yellow"},
    {"word": "оранжевый", "translation": "orange"},
    {"word": "фиолетовый", "translation": "purple"},
    {"word": "розовый", "translation": "pink"},
    {"word": "серый", "translation": "gray"},
    {"word": "коричневый", "translation": "brown"},
    {"word": "бирюзовый", "translation": "turquoise"},
    {"word": "голубой", "translation": "light blue"},
    {"word": "золотистый", "translation": "golden"},
    {"word": "лимонный", "translation": "lemon"},
    {"word": "малиновый", "translation": "raspberry"},
    {"word": "оливковый", "translation": "olive"},
    {"word": "салатовый", "translation": "salad green"},
    {"word": "сиреневый", "translation": "lilac"},
    {"word": "темно-синий", "translation": "navy blue"},
    {"word": "бледно-розовый", "translation": "pale pink"}
]
