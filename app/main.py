from logging import getLogger

from flask import Flask, abort, jsonify, request
from flask.views import MethodView
from sqlalchemy import select

from app.db.models import Product
from app.db.session import async_session
from app.serializers.serializers import BaseSchema
from app.serializers._utils import generate_validator

app = Flask(__name__)

lg = getLogger(__name__)


class ItemAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model
        self.validator: BaseSchema = generate_validator(model, create=True)
        self.view_validator: BaseSchema = generate_validator(model)

    @staticmethod
    def _ret(res): return res if res else abort(404)

    async def _get_item(self, id, session=None):
        if session: return self._ret(await session.get(self.model, id))
        async with async_session() as session:
            return self._ret(await session.get(self.model, id))

    async def get(self, id):
        item = await self._get_item(id)
        return jsonify(self.view_validator.get_one(item))

    async def put(self, id):
        ret, exc = self.validator.default_validate(request.get_json())
        if exc: return jsonify(ret), exc
        async with async_session() as session:
            item = await self._get_item(id, session=session)
            if fk_exc := await self.validator.fk_inner_validation(ret, session): return jsonify(fk_exc), 404
            for k, v in ret.model_dump().items(): setattr(item, k, v)
            await session.commit()
            return jsonify(self.view_validator.get_one(item)), 201

    async def patch(self, id):
        ...

    async def delete(self, id):
        async with async_session() as session:
            item = await self._get_item(id, session=session)
            await session.delete(item)
            await session.commit()
            return "", 204
        
    # async def delete_product(product_id):
    #     async with async_session() as session:
    #         if not (await session.get(Product, product_id)): return jsonify('invalid product'), 404
    #         sales = await session.execute(select(Sale).where(Sale.product_id == product_id))
    #         if sales: return jsonify('sales found'), 400
    #         await session.execute(delete(Product).where(Product.id == product_id))
    #         await session.commit()
    #     return jsonify(), 204


class GroupAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model
        self.validator: BaseSchema = generate_validator(model, create=True)
        self.view_validator: BaseSchema = generate_validator(model)

    async def get(self):
        async with async_session() as session:
            result = await session.execute(select(self.model))
            items = result.scalars().all()
            return jsonify(self.view_validator.get_many(items)), 200

    async def post(self):
        ret, exc = self.validator.default_validate(request.get_json())
        if exc: return jsonify(ret), exc
        async with async_session() as session:
            if fk_exc := await self.validator.fk_inner_validation(ret, session): return jsonify(fk_exc), 404
            product = self.model(**ret.model_dump())
            session.add(product)
            await session.commit()
            return jsonify(self.view_validator.get_one(product)), 201


def register_api(app, model, name):
    item = ItemAPI.as_view(f"{name}-item", model)
    group = GroupAPI.as_view(f"{name}-group", model)
    app.add_url_rule(f"/{name}/<uuid:id>", view_func=item)
    app.add_url_rule(f"/{name}/", view_func=group)

register_api(app, Product, "api/products")
