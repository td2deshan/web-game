from typing import List

from fastapi import Request, WebSocket, APIRouter, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()



@router.get("/dis")
async def chat(request: Request):
    return templates.TemplateResponse('distri/index.html', context={'request': request})


game_data = [i for i in range(100)]  # store game data

portion = 0

@router.websocket("/ws-dis")
async def websocket_endpoint(websocket: WebSocket):

    global portion

    await manager.connect(websocket)

    portion += 10

    try:

        await manager.send_personal_message({'init_data': game_data[portion - 10: portion]}, websocket)  # send init game data to new user

        while True:
            data = await websocket.receive_json() # receive data from client
            print(data)

            await manager.send_personal_message({'personal_data': data}, websocket)

            await manager.broadcast({'broadcast_data': data})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast({"disconnect": client})
        await manager.broadcast({"disconnect": 'client'})
