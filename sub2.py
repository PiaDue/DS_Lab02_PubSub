import asyncio

async def subscribe():
    # Connect to the broker server
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    # Loop to handle multiple subscriptions
    while True:
        # Get user input for a channel to subscribe to
        channel = input("Enter channel to subscribe to (or 'd' for 'done'): ").strip()
        if channel.lower() == 'd':
            break

        # Send the subscription request to the broker
        writer.write(f"{channel}\n".encode())
        await writer.drain()  # Ensure the message is sent

    print("Listening for messages...")

    # Keep listening for messages from the broker
    while True:
        data = await reader.readline()
        if not data:
            break
        print(data.decode().strip())

    # Close the connection
    writer.close()
    await writer.wait_closed()

# Run the subscribe function
asyncio.run(subscribe())
