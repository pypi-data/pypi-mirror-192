from oap_rq import ack_queue_var, active_queue_var, client_addr_var, pending_queue_var


class QueueInfo:
    def __init__(self, redis, *, service, queue):
        self.redis = redis
        self.stage = f"{service}:{queue}:pending"
        self.ack_queue = f"{service}:{queue}:ack"
        self.active_q = f"{service}:{queue}"
        self.create()

    def create(self):
        client_addr_var.set(self.redis)
        ack_queue_var.set(self.ack_queue)
        pending_queue_var.set(self.stage)
        active_queue_var.set(self.active_q)
