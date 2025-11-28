"""
@文件: app.py
@作者: 雷小鸥
@日期: 2025/11/24 12:59
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
import sys
import os
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from logger import logger
import multiprocessing
from multiprocessing.managers import BaseManager
from web.languageTranslations import deepseek


# 创建管理器类
class QueueManager(BaseManager):
    pass


# 注册队列获取方法
QueueManager.register('get_win_props_queue')

# 全局变量
WIN_PROPS_QUEUE = None




def init_queue():
    global WIN_PROPS_QUEUE
    if WIN_PROPS_QUEUE is None:
        try:
            # 连接到管理器
            manager = QueueManager(address=('127.0.0.1', 50000), authkey=b'abc')
            manager.connect()
            WIN_PROPS_QUEUE = manager.get_win_props_queue()
            logger.info("已连接到管理器，队列ID: %s", id(WIN_PROPS_QUEUE))
        except Exception as e:
            logger.error("连接管理器失败: %s", e)
            # 创建本地队列作为fallback
            WIN_PROPS_QUEUE = multiprocessing.Queue(maxsize=5)


# 在应用启动时初始化队列
init_queue()


class TranslationRequest(BaseModel):
    translation: str


BASE_PATH = None
try:
    BASE_PATH = sys._MEIPASS
except Exception:
    BASE_PATH = os.path.abspath(".")

app = FastAPI()

app.mount('/ui', StaticFiles(directory=Path(BASE_PATH) / 'ui-static', html=True), name="ui")


@app.get("/")
async def root():
    return FileResponse(Path(BASE_PATH) / "ui-static/index.html")


@app.post("/api/translation")
async def api_translation(data: TranslationRequest):
    text = data.translation
    res = deepseek.get(text)
    logger.info("翻译文本:", res)
    return res


@app.post('/setting/window/props')
async def set_window_props(request: Request):
    logger.info('post 中内存id: %s', id(WIN_PROPS_QUEUE))

    json_data = await request.json()
    switch = json_data['alwaysOnTop']
    logger.info('tip: %s', switch)

    if WIN_PROPS_QUEUE:
        try:
            WIN_PROPS_QUEUE.put(switch)
            logger.info("成功发送消息到队列")
        except Exception as e:
            logger.error("发送消息到队列失败: %s", e)

    return {"status": "success"}
