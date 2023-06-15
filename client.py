import asyncio
import websockets

async def receive_data():
    async with websockets.connect('ws://localhost:8765') as websocket:
        while True:
            data = await websocket.recv()
            print("Received data:", data)

asyncio.get_event_loop().run_until_complete(receive_data())

