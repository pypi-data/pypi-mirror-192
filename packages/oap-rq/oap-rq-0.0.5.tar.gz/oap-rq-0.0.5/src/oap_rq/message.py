import datetime
from dataclasses import asdict, dataclass, field
from json import dumps

from oap_rq import ack_queue_var, client_addr_var, pending_queue_var
from oap_rq.logger import logger


@dataclass
class Message:
    id: str
    data: dict
    queue: str
    expire_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.expire_at = (
            datetime.datetime.fromisoformat(self.expire_at)
            if isinstance(self.expire_at, str)
            else self.expire_at
        )

    async def ack(self):
        redis = client_addr_var.get()
        ack = ack_queue_var.get()
        consumer = pending_queue_var.get()
        pipe = redis.pipeline()
        pipe.lrem(ack, 0, self.to_json_str())
        pipe.hdel(consumer, self.id)
        await pipe.execute()

        logger.info(
            {
                "message": "sending ack to ack queue",
                "_id": self.id,
                "queue": self.queue,
                **asdict(self),
            }
        )

    def default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    def to_json_str(self):
        return dumps(asdict(self), default=self.default)
