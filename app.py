"""
@文件: app.py
@作者: 雷小鸥
@日期: 2025/11/24 12:59
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from web.languageTranslations import deepseek


class TranslationRequest(BaseModel):
    translation: str


app = FastAPI()

app.mount('/ui', StaticFiles(directory='ui-static', html=True), name="ui")


@app.get("/")
async def root():
    return FileResponse("ui-static/index.html")


@app.post("/api/translation")
async def api_translation(data: TranslationRequest):
    text = data.translation
    res = deepseek.get(text)
    print("翻译文本:", res)
    return res


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
