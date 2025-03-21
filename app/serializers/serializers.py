
from pydantic import UUID4, PositiveFloat

from app.db.models import Category, Product
from app.serializers._s_parents import BaseAttrs, BaseSchema, Edit


class ProductSchema(BaseSchema, BaseAttrs):
    name: str
    price: PositiveFloat
    category_id: UUID4

    class Meta:
        model = Product
        create = False

class ProductCreate(BaseSchema, Edit):
    name: str
    price: PositiveFloat
    category_id: UUID4

    class Meta:
        model = Product
        create = True
    
    async def fk_inner_validation(validated_cls, session):
        if (await session.get(Category, validated_cls.category_id)): return 
        return 'invalid category'
