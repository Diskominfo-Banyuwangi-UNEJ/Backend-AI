"""keramaian

Revision ID: 3ba718bf39af
Revises: 
Create Date: 2025-05-15 13:21:06.106553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ba718bf39af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'USER', 'STAFF', name='roleenum'), nullable=False),
    sa.Column('name_lengkap', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=35), nullable=False),
    sa.Column('no_telepon', sa.String(length=13), nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id_user'),
    sa.UniqueConstraint('email')
    )
    op.create_table('keramaian',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama_lokasi', sa.String(length=35), nullable=False),
    sa.Column('alamat', sa.String(length=35), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tumpukan_sampah',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama_lokasi', sa.String(length=35), nullable=False),
    sa.Column('alamat', sa.String(length=35), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('analisis_keramaian',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_keramaian', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Enum('SEPI', 'NORMAL', 'PADAT', name='statusanalisiskeramaian'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id_keramaian'], ['keramaian.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('analisis_tumpukan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_tumpukan', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Enum('OK', 'FULL', name='statusanalisis'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id_tumpukan'], ['tumpukan_sampah.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('analisis_tumpukan')
    op.drop_table('analisis_keramaian')
    op.drop_table('tumpukan_sampah')
    op.drop_table('keramaian')
    op.drop_table('User')
    # ### end Alembic commands ###
