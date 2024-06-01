from marshmallow import Schema, fields

class AdminSchema(Schema):
    id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)

class ImageSchema(Schema):
    id = fields.Int(required=True)
    image_url = fields.Str(required=True)
    # image_blob = fields.Method("get_image_blob", deserialize="load_image_blob")

    # def get_image_blob(self, obj):
    #     return obj.image_blob.decode('latin-1')

    # def load_image_blob(self, value):
    #     return value.encode('latin-1')

class ProductSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    stock_quantity = fields.Int(required=True)
    images = fields.List(fields.Nested(ImageSchema), required=True)

class OrderSchema(Schema):
    id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    delivery_address = fields.Str(required=True)
    amount = fields.Float(required=True)
    status = fields.Str(required=True)
    order_date = fields.DateTime(required=True)
    products = fields.List(fields.Nested(ProductSchema), required=True)
