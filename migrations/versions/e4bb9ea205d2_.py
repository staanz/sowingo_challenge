"""empty message

Revision ID: e4bb9ea205d2
Revises: 
Create Date: 2021-03-04 11:43:55.263344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4bb9ea205d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('permission_class', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    op.create_table('vacations',
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vacation_start', sa.DateTime(timezone=True), nullable=False),
    sa.Column('vacation_end', sa.DateTime(timezone=True), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('requester_id', sa.Integer(), nullable=False),
    sa.Column('validator_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['requester_id'], ['users.id'], name=op.f('fk_vacations_requester_id_users')),
    sa.ForeignKeyConstraint(['validator_id'], ['users.id'], name=op.f('fk_vacations_validator_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_vacations'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacations')
    op.drop_table('users')
    # ### end Alembic commands ###