from abc import ABC, abstractmethod
from datetime import datetime as dt
from typing import Optional, Union

from pydantic import UUID4, BaseModel, ConfigDict, TypeAdapter, ValidationError


class Edit(ABC):
    @staticmethod
    @abstractmethod
    async def fk_inner_validation(validated_cls, session): return True


class BaseAttrs:
    id: UUID4
    created_at: dt
    updated_at: dt


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    class Meta:
        abstract = True
        model = None
        create = None

    @classmethod
    def get_one(cls, obj):
        product_schema = cls.model_validate(obj)
        return product_schema.model_dump()

    @classmethod
    def get_many(cls, qs):
        adapter = TypeAdapter(list[cls])
        return adapter.dump_python(qs)

    @classmethod
    def default_validate(cls, data: dict) -> tuple[Union[BaseModel, dict], Optional[int]]:
        try: return cls.model_validate(data,), None
        except ValidationError as e:
            errors = {}
            for error in e.errors():
                loc = error['loc']
                msg = error['msg']
                field = '.'.join(map(str, loc))
                if field not in errors:
                    errors[field] = []
                errors[field].append(msg)
            return {"detail": errors}, 400