import sqladmin
import wtforms

from api.models.products import Purchase


class PurchaseForm(wtforms.Form):
    steam_id = wtforms.StringField()
    product_id = wtforms.IntegerField()


class PurchaseAdmin(sqladmin.ModelView, model=Purchase):
    form = PurchaseForm
    column_list = [Purchase.steam_id, Purchase.product_id]
