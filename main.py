import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api import mainApi, gameApi

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return {"message": "Hi"}


@app.get("/site", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "hi"})


def configure():
    # app.include_router(mainApi.router)
    app.include_router(gameApi.router)


configure()

#
# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port=5000)
