import uuid

import fastapi
import pydantic
import sqlalchemy as sqla
from sqlalchemy.orm import Session

from api.auth import check_authorization
from api.db import get_db_session
from api.models.products import Purchase, Product

router = fastapi.APIRouter()


class ItemsRequest(pydantic.BaseModel):
    user_steam_ids: list[str]
    product_type: str


class Item(pydantic.BaseModel):
    steam_id: str
    product_name: str
    product_meta: dict


class PurchasedItems(pydantic.BaseModel):
    items: list[Item]


@router.post('/purchased_items', response_model=PurchasedItems)
async def purchased_items(
        request: ItemsRequest,
        session: Session = fastapi.Depends(get_db_session),
        auth: str = fastapi.Depends(check_authorization)
) -> PurchasedItems:

    purchases: list[sqla.Row] = (
        session.query(
            Purchase.steam_id,
            Product.name,
            Product.meta
        ).join(Purchase).filter(
            Product.type == request.product_type
        ).filter(
            Purchase.steam_id.in_(request.user_steam_ids)
        ).all()
    )

    return PurchasedItems(
        items=[
            Item(
                steam_id=steam_id,
                product_name=product_name,
                product_meta=product_meta,
            )
            for (steam_id, product_name, product_meta) in purchases
        ]
    )
