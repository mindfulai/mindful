"""sentiment

Revision ID: b29613ce472b
Revises: 
Create Date: 2018-12-06 17:28:36.215224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b29613ce472b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sentiment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('language', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('faceboot_posts', sa.Column('sentiment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'faceboot_posts', 'sentiment', ['sentiment_id'], ['id'])
    op.alter_column('flask_dance_oauth', 'provider_user_id',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.add_column('moods', sa.Column('sentiment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'moods', 'sentiment', ['sentiment_id'], ['id'])
    op.add_column('tweet_mentions', sa.Column('sentiment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tweet_mentions', 'sentiment', ['sentiment_id'], ['id'])
    op.add_column('tweets', sa.Column('sentiment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tweets', 'sentiment', ['sentiment_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tweets', type_='foreignkey')
    op.drop_column('tweets', 'sentiment_id')
    op.drop_constraint(None, 'tweet_mentions', type_='foreignkey')
    op.drop_column('tweet_mentions', 'sentiment_id')
    op.drop_constraint(None, 'moods', type_='foreignkey')
    op.drop_column('moods', 'sentiment_id')
    op.alter_column('flask_dance_oauth', 'provider_user_id',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.drop_constraint(None, 'faceboot_posts', type_='foreignkey')
    op.drop_column('faceboot_posts', 'sentiment_id')
    op.drop_table('sentiment')
    # ### end Alembic commands ###