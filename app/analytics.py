from datetime import datetime as dt
from typing import Optional

from flask import Blueprint, abort, jsonify, request
from sqlalchemy.sql import func, select

from app.db.models import Product, Sale
from app.db.session import async_session

analytics_api = Blueprint('analytics', __name__, url_prefix='/api/sales')


def query_parser(request, limit=False) -> tuple[dt, dt, Optional[int]]:
    a, tl, dstr = request.args, '%Y-%m-%d', dt.strptime
    try: return dstr(a['start_date'], tl), dstr(a['end_date'], tl), a['limit'] if limit else None
    except (KeyError, ValueError) as e: abort(400, f'{e}')

@analytics_api.get('/total')
async def get_sales_total():
    start, end, _ = query_parser(request)
    async with async_session() as session:
        stmt = (select(func.sum(Sale.quantity).filter(Sale.sale_date.between(start, end))))
        result = await session.execute(stmt)
        total = result.scalars().all()
        return total, 200
        

@analytics_api.get('/top-products')
async def get_top_products():
    limit = None
    start, end, limit = query_parser(request, limit=True)
    async with async_session() as session:
        stmt = (
            select(
                Product.id.label('id'),
                Product.created_at.label('created_at'),
                Product.updated_at.label('updated_at'),
                Product.category_id.label('category_id'),
                Product.name.label('name'),
                func.sum(Sale.quantity).label('total_quantity')
            )
            .outerjoin(Sale, Product.id == Sale.product_id)
            .where(Sale.quantity >= 0, Sale.sale_date.between(start, end))
            .group_by(Product.id)
            .order_by(func.sum(Sale.quantity).desc()).limit(limit)
        )

        result = await session.execute(stmt)
        return jsonify(list(map(dict, result.mappings().all()))), 200
