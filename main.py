from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="build/static"), name="static")

# 返回 React 编译后的主页
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("build/index.html") as f:
        return HTMLResponse(content=f.read())
