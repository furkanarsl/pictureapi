from tortoise.models import Model
from tortoise import fields

from src.models import User


class Log(Model):
    id = fields.IntField(pk=True, null=False)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name='user')
    picture_path = fields.TextField()
    result = fields.TextField()
