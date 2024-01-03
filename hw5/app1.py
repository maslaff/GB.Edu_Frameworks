from fastapi import FastAPI, Request, Form, status
from typing import Optional
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="hw5/templates")


class Item(BaseModel):
    # thing_id: int
    name: str
    thing_type: Optional[str] = "Common"
    description: str
    active: bool = True


# things: list[Item] = []
things: dict[int:Item] = {}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "main.html", {"request": request, "things": things}
    )


@app.post("/")
async def add_thing_item(
    request: Request,
    name: str = Form(...),
    thing_type: str = Form(...),
    description: str = Form(...),
):
    i_id = max(things) + 1 if len(things) else 0
    thing = Item(name=name, thing_type=thing_type, description=description, active=True)
    things[i_id] = thing
    return RedirectResponse(
        request.url_for("root"), status_code=status.HTTP_303_SEE_OTHER
    )


@app.put("/edit/{thing_id}")
async def edit_thing_item(
    request: Request,
    thing_id: int,
    name: str = None,
    thing_type: str = None,
    description: str = None,
):
    if things.get(thing_id):
        if name:
            things[thing_id].name = name
        if thing_type:
            things[thing_id].thing_type = thing_type
        if description:
            things[thing_id].description = description
        return RedirectResponse(
            request.url_for("root"), status_code=status.HTTP_303_SEE_OTHER
        )
    return RedirectResponse(
        request.url_for("root"), status_code=status.HTTP_404_NOT_FOUND
    )


@app.delete("/remove/{thing_id}")
async def delete_thing_item(
    request: Request,
    thing_id: int,
):
    if things.get(thing_id):
        things[thing_id].active = False
    return RedirectResponse(
        request.url_for("root"), status_code=status.HTTP_303_SEE_OTHER
    )
