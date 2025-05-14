from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "welcome.html", {"request": request, "title": "Главная страница"}
    )

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        "register.html", {"request": request, "title": "Регистрация"}
    )

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "title": "Вход"}
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "title": "Страница не найдена"},
            status_code=404
        )
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "title": "Ошибка", "code": exc.status_code},
        status_code=exc.status_code
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
