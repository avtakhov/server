import fastapi
import pydantic
from sqlalchemy.orm import Session

from api.auth import check_authorization
from api.db import get_db_session
from api.models.products import Purchase, Product
from api.models.users import User

router = fastapi.APIRouter()


class PurchaseRequest(pydantic.BaseModel):
    steam_id: str
    product_type: str
    product_name: str


class PurchaseResponse(pydantic.BaseModel):
    new_amount: int


@router.post('/purchase', response_model=PurchaseResponse)
async def purchase(
        request: PurchaseRequest,
        session: Session = fastapi.Depends(get_db_session),
        auth: str = fastapi.Depends(check_authorization)
):
    (product_id, price, ) = session.query(Product.product_id, Product.price).filter(
        Product.type == request.product_type
    ).filter(Product.name == request.product_name).one()

    user = session.query(User).filter(
        User.steam_id == request.steam_id
    ).one()

    new_amount = user.amount - price
    user.amount = new_amount
    session.add(user)
    session.add(
        Purchase(
            steam_id=request.steam_id,
            product_id=product_id,
        )
    )
    session.commit()

    return PurchaseResponse(new_amount=new_amount)

