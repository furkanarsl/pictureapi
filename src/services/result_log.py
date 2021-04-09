from src.models.log import Log


class LogService:
    async def create(self, user_id, result, picture_path):
        log = await Log.create(user_id=user_id, result=result, picture_path=picture_path)
        return log

log_service = LogService()
