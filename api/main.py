from fastapi import FastAPI
from sqladmin import Admin

import api.purchased_items
import api.purchase
import api.products
import api.users
from .auth import AdminAuth
from .db import get_engine
from .admin.products import ProductAdmin
from .admin.purchases import PurchaseAdmin
from .settings import settings

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})
app.include_router(api.purchased_items.router)
app.include_router(api.purchase.router)
app.include_router(api.products.router)
app.include_router(api.users.router)

admin = Admin(app, get_engine(), authentication_backend=AdminAuth(secret_key=settings.secret_key))
admin.add_view(ProductAdmin)
admin.add_view(PurchaseAdmin)
