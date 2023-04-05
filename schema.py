from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) # never sent back to client


class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)