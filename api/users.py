import fastapi
import pydantic
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from api.auth import check_authorization
from api.db import get_db_session
from api.models.products import Product
from api.models.users import User

router = fastapi.APIRouter()


class UserModel(pydantic.BaseModel):
    steam_id: str
    amount: int


class UsersResponse(pydantic.BaseModel):
    users: list[UserModel]


class UserUpdate(pydantic.BaseModel):
    steam_id: str
    to_add: int


class UsersRequest(pydantic.BaseModel):
    users: list[UserUpdate]


@router.post('/users', response_model=UsersResponse)
async def users(
        request: UsersRequest,
        session: Session = fastapi.Depends(get_db_session),
        auth: str = fastapi.Depends(check_authorization)
):
    if not request.users:
        raise fastapi.HTTPException(status_code=400)

    user_data = [
        {'steam_id': user.steam_id, 'amount': user.to_add, }
        for user in request.users
    ]

    upsert_stmt = insert(User).values(user_data)
    upsert_stmt = upsert_stmt.on_conflict_do_update(
        index_elements=[User.steam_id],
        set_=dict(amount=User.amount + upsert_stmt.excluded.amount),
    ).returning(User.steam_id, User.amount)

    db_users = session.execute(upsert_stmt).fetchall()
    session.commit()

    return UsersResponse(
        users=[
            UserModel(steam_id=steam_id, amount=amount)
            for (steam_id, amount) in db_users
        ]
    )
