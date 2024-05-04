import sqlalchemy as sqla

from api.db import Base


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = (
        sqla.CheckConstraint('price >= 0'),
        sqla.UniqueConstraint('type', 'name'),
        sqla.Index('type', 'name')
    )

    product_id = sqla.Column(sqla.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    price = sqla.Column(sqla.BigInteger(), nullable=False)
    type = sqla.Column(sqla.String, nullable=False)
    name = sqla.Column(sqla.String)
    meta = sqla.Column(sqla.JSON, nullable=True)


class Purchase(Base):
    __tablename__ = 'purchases'
    __table_args__ = (
        sqla.UniqueConstraint('steam_id', 'product_id'),
    )

    purchase_id = sqla.Column(sqla.BigInteger, nullable=False, primary_key=True, autoincrement=True)
    product_id = sqla.Column(sqla.BigInteger, sqla.ForeignKey('products.product_id'), nullable=False)
    steam_id = sqla.Column(sqla.String, sqla.ForeignKey('users.steam_id'), nullable=False)

