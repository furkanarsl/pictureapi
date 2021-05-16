from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True, null=False)
    name = fields.TextField(null=True)
    last_name = fields.TextField(null=True)
    email = fields.CharField(max_length=100, unique=True, index=True, null=False)
    hashed_password = fields.TextField(null=False)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    class PydanticMeta:
        exclude = ["is_superuser"]