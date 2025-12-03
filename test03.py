"""
@文件: test03.py
@作者: 雷小鸥
@日期: 2025/11/29 23:00
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
from uvicorn import run
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# 静态文件目录路径
static_dir = os.path.join(os.path.dirname(__file__), "ui")

# 挂载静态文件
app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="assets")


@app.get("/")
async def index():
    return FileResponse('./ui/index.html')


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)
