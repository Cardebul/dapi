"""first

Revision ID: 4e56c1f88b64
Revises: 
Create Date: 2025-03-18 17:55:12.175767

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4e56c1f88b64'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _base_data_insert(sales_min = 7, sales_max = 255):
    from datetime import datetime as dt
    from datetime import timedelta
    from random import randint
    from uuid import uuid4

    base_gen = lambda: {'id': str(uuid4()), 'created_at': dt.now(), 'updated_at': dt.now()}
    
    ELECTRONICS = 'Electronics'
    CLOTHING = 'Clothing'
    BOOKS = 'Books'
    PRODUCT_NAMES = {
        ELECTRONICS: ['Laptop','Smartphone','Tablet','Smartwatch','Headphones',],
        CLOTHING: ['T-shirt', 'Jeans','Jacket','Sweater','Sneakers',],
        BOOKS: ['Novel','Textbook','Biography','Cookbook','Comics',],
    }

    categories = [{**base_gen(), 'name': i} for i in [ELECTRONICS, CLOTHING, BOOKS]]

    products = []
    for category in categories:
        for product_name in PRODUCT_NAMES[category['name']]:
            products.append({**base_gen(), 'name': product_name, 'category_id': category['id']})

    sales = []
    cur_date = dt.now()
    six_m_ago = cur_date - timedelta(days=180)

    for product in products:
        num_sales = randint(sales_min, sales_max)
        for _ in range(num_sales):
            sale_date = six_m_ago + timedelta(days=randint(0, 180))
            sales.append({
                **base_gen(),
                'product_id': product['id'],
                'quantity': randint(1, 20),
                'sale_date': sale_date
            })

    meta = sa.MetaData()
    bind = op.get_bind()
    op.bulk_insert(sa.Table('category', meta, autoload_with=bind), categories)
    op.bulk_insert(sa.Table('product', meta, autoload_with=bind), products)
    op.bulk_insert(sa.Table('sale', meta, autoload_with=bind), sales)

def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('product',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('category_id', sa.Uuid(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sale',
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('sale_date', sa.DateTime(), nullable=False),
    sa.Column('product_id', sa.Uuid(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


    # Base data insert
    _base_data_insert()
    # ### end Base data insert




def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sale')
    op.drop_table('product')
    op.drop_table('category')
    # ### end Alembic commands ###
