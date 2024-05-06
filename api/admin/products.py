import json

import sqladmin
import wtforms

from api.models.products import Product


def filter_json(data):
    if isinstance(data, dict):
        return json.dumps(data)
    else:
        return json.loads(data) if data else None


class JSONField(wtforms.TextAreaField):
    def wrap_formdata(self, form, formdata):
        if formdata is not None and not hasattr(formdata, "getlist"):
            if hasattr(formdata, "getall"):
                return formdata
            else:
                raise TypeError(
                    "formdata should be a multidict-type wrapper that"
                    " supports the 'getlist' method"
                )
        return formdata


class ProductAdmin(sqladmin.ModelView, model=Product):
    form_columns = [Product.name, Product.type, Product.price, Product.meta]
    form_overrides = dict(meta=JSONField)
    form_args = dict(meta={"filters": [filter_json]})

    column_list = [Product.product_id, Product.name, Product.type]
