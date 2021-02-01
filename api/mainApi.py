from fastapi import Request, WebSocket, APIRouter
from fastapi.templating import Jinja2Templates

from service.apiService import call_api, ebay_api, amazon_api, aliexpress_api

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/chat")
async def chat(request: Request):
    return templates.TemplateResponse('chat.html', context={'request': request})


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # data = await websocket.receive_json()
        print(data)
        # await websocket.send_text(f"Message text was: {data}")

        # await websocket.send_json({'ebay': '<h1>ebay</h1>'})
        # await websocket.send_json({'amazon': '<h4>amazon</h4>'})
        # await websocket.send_json({'aliexpress': '<h2>aliexpress</h2>'})

        # eb = await call_api('https://td2deshan.github.io/ese.github.io/')
        # al = await call_api('https://td2deshan.github.io/ese.github.io/')

        ebay_data = await ebay_api('https://td2deshan.github.io/ese.github.io/')
        aliexpress_data = await aliexpress_api('https://td2deshan.github.io/ese.github.io/')
        amazon_data = await amazon_api('https://td2deshan.github.io/ese.github.io/')

        await websocket.send_json({'ebay': ebay_data})
        await websocket.send_json({'aliexpress': aliexpress_data})
        await websocket.send_json({'amazon': amazon_data})
