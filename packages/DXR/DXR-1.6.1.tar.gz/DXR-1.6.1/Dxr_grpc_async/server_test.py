from streaming.server import Stream_server
import asyncio

streaming_server = Stream_server('0.0.0.0', 50051)
asyncio.run(streaming_server.start())