import asyncio

async def publish():
    while True:
        # Connect to the broker server
        reader, writer = await asyncio.open_connection('127.0.0.1', 8889)

        # Get user input for channel and message
        channel = input("Enter channel name (press 'q' to quit): ")
        if channel == 'q':
            break
        message = input("Enter message: ")

        # Send the message to the broker
        writer.write(f"{channel};{message}\n".encode())

        # Close the connection
        writer.close()
        await writer.wait_closed()

# Run the publish function asynchronously
asyncio.run(publish())
