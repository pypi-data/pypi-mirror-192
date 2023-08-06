import datetime
import uuid

from oap_rq.logger import logger
from oap_rq.message import Message
from oap_rq.monitor import Receiver
from oap_rq.q_info import QueueInfo


class OAPSendError(Exception):
    ...


class RedisQueue(QueueInfo):
    def __init__(self, redis, *, service="notify", queue="test"):
        super().__init__(redis, service=service, queue=queue)

    async def send(self, data, timeout=5):
        try:
            expire_at: datetime = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=timeout
            )
            msg = Message(
                id=uuid.uuid4().hex, data=data, queue=self.active_q, expire_at=expire_at
            )
            pipe = self.redis.pipeline()
            pipe.hset(self.stage, msg.id, msg.to_json_str())
            pipe.lpush(self.active_q, msg.to_json_str())
            await pipe.execute()
            logger.info({"message": {"id": msg.id, "status": "sent"}, **data})
            return msg.id
        except Exception as err:  # noqa
            raise OAPSendError(f"Send Message Error {err}")

    def sync_send(self, data, timeout=5):
        """non async call"""
        try:
            expire_at: datetime = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=timeout
            )
            msg = Message(
                id=uuid.uuid4().hex, data=data, queue=self.active_q, expire_at=expire_at
            )
            pipe = self.redis.pipeline()
            pipe.hset(self.stage, msg.id, msg.to_json_str())
            pipe.lpush(self.active_q, msg.to_json_str())
            pipe.execute()
            return msg.id
        except Exception as err:  # noqa
            raise OAPSendError(f"Send Message Error {err}")

    async def receive(self, worker):
        async for f in Receiver().receive(worker):
            yield f
