from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from server import LayoutViewServer
from pathlib import Path


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

gdsfiles = StaticFiles(directory="gds_files")
app.mount("/gds_files", gdsfiles, name="gds_files")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/gds/{id}", response_class=HTMLResponse)
async def gds_view(request: Request, id: str):
    return templates.TemplateResponse(
        "client.html", {"request": request, "id": id.strip(".gds")}
    )


@app.websocket("/gds/{id}/ws")
async def gds_ws(websocket: WebSocket, id: str):
    await websocket.accept()
    print(id)
    if gdsfiles is not None:

        print(f"{id.replace('.gds','')}")
        lvs = LayoutViewServer(
            str(Path(gdsfiles.directory) / f"{id.replace('.gds','')}.gds")
        )
        while True:
            await lvs.connection(websocket)
