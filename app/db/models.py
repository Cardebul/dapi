import uuid
from datetime import datetime as dt
from typing import List

from sqlalchemy import DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created_at: Mapped[dt] = mapped_column(DateTime(), default=func.now())
    updated_at: Mapped[dt] = mapped_column(DateTime(), default=func.now(), onupdate=func.now())


class Category(Base):
    __tablename__ = 'category'

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    products: Mapped[List['Product']] = relationship(back_populates='category')


class Product(Base):
    __tablename__ = 'product'

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    category: Mapped['Category'] = relationship(back_populates='products')
    sales: Mapped[List['Sale']] = relationship(back_populates='product')



class Sale(Base):
    __tablename__ = 'sale'

    quantity: Mapped[int] = mapped_column(nullable=False)
    sale_date: Mapped[dt] = mapped_column(DateTime(), nullable=False)

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('product.id', ondelete='RESTRICT'), nullable=False)
    product: Mapped['Product'] = relationship(back_populates='sales')


