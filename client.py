import timeit


# import asyncio
# import websockets
#
# async def receive_data():
#     async with websockets.connect('ws://localhost:8765') as websocket:
#         symbol = input("Enter a symbol: ")
#         await websocket.send(symbol)
#         while True:
#             data = await websocket.recv()
#             print("Received data:", data)
#
# asyncio.get_event_loop().run_until_complete(receive_data())
#

def reverse_string_recur(s: str):
    if s == '':
        return s
    else:
        return s[-1] + reverse_string_recur(s[:len(s) - 1])


def reverse_string_iter(s: str):
    new_str = ''
    for i in range(len(s) - 1, -1, -1):
        new_str += s[i]
    return new_str