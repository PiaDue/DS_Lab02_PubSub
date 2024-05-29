import asyncio

class MessageBroker:
    def __init__(self):
        self.channels = {}  # Dictionary to store channels and their subscribers

    async def handle_publisher(self, reader, writer):
        # Handle connections from publishers
        data = await reader.read(100)
        message = data.decode().strip()
        if ';' in message:
            channel, message = message.split(';', 1)  # Split message into channel and message
            print(f"Received message for channel '{channel}': {message}")  # Print received message
            await self.publish(channel, message)
        writer.close()

    async def handle_subscriber(self, reader, writer):
        # Handle connections from subscribers
        while True:
            data = await reader.read(100)
            if not data:
                break
            channel = data.decode().strip()
            if channel not in self.channels:
                self.channels[channel] = []
            self.channels[channel].append(writer)
            print(f"New subscriber connected to channel '{channel}'")

    async def publish(self, channel, message):
        # Publish a message to a channel and distribute it to subscribers
        if channel in self.channels:
            for subscriber in self.channels[channel]:
                subscriber.write(f"{channel}: {message}\n".encode())
                await subscriber.drain()

async def main():
    broker = MessageBroker()  # Create an instance of the message broker
    
    # Start a server for subscribers
    subscriber_server = await asyncio.start_server(
        broker.handle_subscriber, '127.0.0.1', 8888)
    
    # Start a server for publishers
    publisher_server = await asyncio.start_server(
        broker.handle_publisher, '127.0.0.1', 8889)
    
    print("Broker server running.")
    print("Subscriber server listening on 127.0.0.1:8888")
    print("Publisher server listening on 127.0.0.1:8889")
    
    async with subscriber_server, publisher_server:
        await asyncio.gather(subscriber_server.serve_forever(), publisher_server.serve_forever())

# Run the main function asynchronously
asyncio.run(main())
