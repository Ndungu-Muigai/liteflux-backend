from marshmallow import Schema, fields

class AdminSchema(Schema):
    id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)

class ImageSchema(Schema):
    id = fields.Int(required=True)
    image_name = fields.Str(required=True)
    image_url=fields.Str(required=True)

class ProductSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    stock_quantity = fields.Int(required=True)
    images = fields.List(fields.Nested(ImageSchema), required=True)

class OrderProductsSchema(Schema):
    id=fields.Int(required=True)
    product_id=fields.Int(required=True)
    order_id=fields.Int(required=True)
    quantity=fields.Int(required=True)

class OrderSchema(Schema):
    id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    county = fields.Str(required=True)
    sub_county = fields.Str(required=True)
    ward = fields.Str(required=True)
    street = fields.Str(required=True)
    amount = fields.Float(required=True)
    status = fields.Str(required=True)
    order_date = fields.DateTime(required=True)
    products = fields.Nested((OrderProductsSchema),required=True)
