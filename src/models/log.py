from tortoise.models import Model
from tortoise import fields

from src.models import User


class Log(Model):
    id = fields.IntField(pk=True, null=False)
    query_date = fields.DatetimeField(auto_now=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name='user')
    picture_path = fields.TextField()
    result = fields.TextField()

    def img_path(self) -> str:
        return self.picture_path.replace("\\", "/")

    class PydanticMeta:
        exclude = ['id', "picture_path"]
        computed = ["img_path"]
