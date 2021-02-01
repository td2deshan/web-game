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


@router.get('/game-login')
async def game_login(request: Request):
    return templates.TemplateResponse('game/gameLogin.html', context={'request': request})


@router.get("/game")
async def chat(request: Request):
    return templates.TemplateResponse('game/game.html', context={'request': request})


game_data = []


@router.websocket("/game/{client}")
async def websocket_endpoint(websocket: WebSocket, client: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            game_data.append(data)
            await manager.send_personal_message({'my': data}, websocket)

            await manager.broadcast({'game_data': game_data})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"disconnect": client})