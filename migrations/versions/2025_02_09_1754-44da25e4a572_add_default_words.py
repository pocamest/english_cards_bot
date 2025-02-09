"""Add default words

Revision ID: 44da25e4a572
Revises: d4312389ec07
Create Date: 2025-02-09 17:54:38.965133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44da25e4a572'
down_revision: Union[str, None] = 'd4312389ec07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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


def upgrade() -> None:
    default_words_table = sa.table(
        'default_words',
        sa.Column('word', sa.String(255), nullable=False),
        sa.Column('translation', sa.String(255), nullable=False)
    )
    op.bulk_insert(default_words_table, DEFAULT_WORDS)


def downgrade() -> None:
    default_words = sa.table(
        'default_words',
        sa.column('word', sa.String)
    )

    words_to_delete = [word["word"] for word in DEFAULT_WORDS]

    op.execute(
        default_words.delete().where(
            default_words.c.word.in_(words_to_delete)
        )
    )
