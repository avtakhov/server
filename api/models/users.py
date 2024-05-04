import sqlalchemy as sqla

from api.db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        sqla.CheckConstraint('amount >= 0', name='amount_positive_check'),
    )

    steam_id = sqla.Column(sqla.String, nullable=False, primary_key=True)
    amount = sqla.Column(sqla.BigInteger(), nullable=False, default=10_000)
