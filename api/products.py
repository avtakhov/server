import fastapi
import pydantic
from sqlalchemy.orm import Session

from api.auth import check_authorization
from api.db import get_db_session
from api.models.products import Product

router = fastapi.APIRouter()


class ProductModel(pydantic.BaseModel):
    product_name: str
    price: int
    meta: dict


class Products(pydantic.BaseModel):
    products: list[ProductModel]


@router.get('/products', response_model=Products)
async def products(
        product_type: str = fastapi.Query(),
        session: Session = fastapi.Depends(get_db_session),
        auth: str = fastapi.Depends(check_authorization)
):
    result = session.query(
        Product.name,
        Product.price,
        Product.meta
    ).filter(Product.type == product_type).all()

    return Products(
        products=[
            ProductModel(product_name=name, price=price, meta=meta)
            for (name, price, meta, ) in result
        ]
    )
