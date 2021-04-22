from src.models.log import Log
from src.schemas.log import LogSchemaList


class LogService:
    async def create(self, user_id, result, picture_path):
        log = await Log.create(user_id=user_id, result=result, picture_path=picture_path)
        return log

    async def get_logs_by_user(self, user_id: int, skip: int, limit: int) -> LogSchemaList:
        return await LogSchemaList.from_queryset(
            Log.filter(user_id=user_id).order_by('-query_date').limit(limit=limit).offset(offset=skip))
        # return await Log.filter(user_id=user_id).order_by('-query_date').all()

    async def get_log_by_img(self, img_name: str):
        return await Log.filter(picture_path=img_name).first()


log_service = LogService()
