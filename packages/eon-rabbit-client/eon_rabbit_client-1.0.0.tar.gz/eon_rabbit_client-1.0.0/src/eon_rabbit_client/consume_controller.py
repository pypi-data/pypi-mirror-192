from inspect import iscoroutinefunction as isAsync
import json
from aio_pika import IncomingMessage
from eon_rabbit_client.channel_controller import ChannelController


async def await_if_async(func, *args):
    if func:
        await func(*args) if isAsync(func) else func(*args)


def body_to_json(messageArgs):
    try:
        messageArgs["body"] = messageArgs["body"].decode()
        messageArgs["body"] = json.loads(messageArgs["body"])

    except json.decoder.JSONDecodeError:
        body = messageArgs["body"]
        raise Exception(f"({body}) is not a valid JSON")


def create_handler(handler):
    async def message_handler(message: IncomingMessage):
        async def ack():
            await message.ack()
        async def reject():
            await message.nack(requeue=False)
        async def requeue():
            await message.nack(requeue=True)
        messageArgs = {
            "body": message.body,
            "routing_key": message.routing_key,
            "exchange": message.exchange,
            "ack": ack,
            "reject": reject,
            "requeue": requeue,
        }
        try:
            body_to_json(messageArgs)
        except Exception as err:
            await message.nack(requeue=False)
            raise err
        await await_if_async(handler, messageArgs)

    return message_handler


class ConsumeController:
    def __init__(self, channel_controller: ChannelController):
        self.channel_controller = channel_controller

    async def consume(self, queue_name, handler):
        channel = await self.channel_controller.get_channel()
        queue = await channel.get_queue(queue_name)

        print(f"Consuming: {queue_name}")
        message_handler = create_handler(handler)

        return await queue.consume(message_handler)
