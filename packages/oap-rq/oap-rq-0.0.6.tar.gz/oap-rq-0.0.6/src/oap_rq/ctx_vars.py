import contextvars

client_addr_var = contextvars.ContextVar("client_addr")
ack_queue_var = contextvars.ContextVar("consumer_ack")
pending_queue_var = contextvars.ContextVar("consumer_current")
active_queue_var = contextvars.ContextVar("active_queue")
