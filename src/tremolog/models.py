from tortoise.models import Model
from tortoise import Tortoise, fields


class Posts(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField(max_length=240)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "posts"

    def __str__(self):
        return self.text


async def init(db_url):
    await Tortoise.init(db_url=str(db_url), modules={"models": ["tremolog.models"]})
    await Tortoise.generate_schemas()
