"""
@文件: window.py
@作者: 雷小鸥
@日期: 2025/11/24 12:59
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
import webview
import uvicorn
import multiprocessing
import time

import app

def run_app():
    # 禁用 reload，避免子进程异常
    uvicorn.run(app.app, host="127.0.0.1", port=8000, reload=False)



if __name__ == "__main__":
    # 启动 Uvicorn 服务进程
    app_process = multiprocessing.Process(target=run_app)
    app_process.start()

    time.sleep(0.5)

    # 启动 WebView 窗口（会阻塞直到窗口关闭）
    webview.create_window('Simple browser', 'http://127.0.0.1:8000')
    webview.start()

    # 可选：窗口关闭后终止后台服务
    app_process.terminate()
    app_process.join()


