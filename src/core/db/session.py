from redis import StrictRedis
from src.core.config import settings


redis_email = StrictRedis(
    host=settings.REDIS_URL,
    port=settings.REDIS_PORT,
    db=0,
    encoding="UTF-8",
    charset="utf-8",
    decode_responses=True,
)
redis_pw = StrictRedis(
    host=settings.REDIS_URL,
    port=settings.REDIS_PORT,
    db=1,
    encoding="UTF-8",
    charset="utf-8",
    decode_responses=True,
)
