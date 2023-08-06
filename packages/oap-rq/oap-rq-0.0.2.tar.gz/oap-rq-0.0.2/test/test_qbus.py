import pytest

from oap_rq.q import QBus


@pytest.mark.asyncio
async def test_simple_send_receive(redis):
    q = QBus(redis, service="test", queue="customer-food")

    @q.consumer(name="ff")
    async def process(event):
        async for e in event:
            assert e.data == {"test": "me"}
            break

    await q.send({"test": "me"})

    await process()
