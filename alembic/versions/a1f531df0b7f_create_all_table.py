"""create_all_table

Revision ID: a1f531df0b7f
Revises: 
Create Date: 2024-10-24 23:06:54.600501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1f531df0b7f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoices',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('invoice_code', sa.String(), nullable=True),
    sa.Column('customer_name', sa.String(), nullable=True),
    sa.Column('walk_in_customer', sa.String(), nullable=True),
    sa.Column('current_date', sa.String(), nullable=False),
    sa.Column('grand_total', sa.Float(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('receiving_amount', sa.Float(), nullable=True),
    sa.Column('remaining_amount', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('barcode', sa.String(), nullable=True),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('rank_number', sa.String(), nullable=True),
    sa.Column('pur_price', sa.Float(), nullable=True),
    sa.Column('sel_price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_table('invoice_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('invoice_id', sa.Integer(), nullable=False),
    sa.Column('product_code', sa.String(length=255), nullable=True),
    sa.Column('product_name', sa.String(length=255), nullable=True),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('company', sa.String(length=255), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('sell_price', sa.Float(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoice_items')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    op.drop_table('invoices')
    # ### end Alembic commands ###