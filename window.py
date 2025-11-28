"""
@文件: window.py
@作者: 雷小鸥
@日期: 2025/11/24 12:59
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
import threading
import webview
import uvicorn
import multiprocessing
from multiprocessing.managers import BaseManager
import time
import sys
from logger import logger
from app import QueueManager

# 创建锁
WIN_PROPS_LOCK = threading.Lock()

PORT_QUEUE = None
APP_RUNNING = True

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    logger.info("运行于 PyInstaller 打包环境")
    logger.info(sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] == 'child':
        logger.info("子进程，跳过主程序逻辑")
        sys.exit()


def run_app(port_queue: multiprocessing.Queue):
    from app import app
    # 禁用 reload，避免子进程异常
    config = uvicorn.Config(app, host="127.0.0.1", port=0, reload=False)
    server = uvicorn.Server(config)

    # 获取 socket 并绑定（这样能拿到实际端口）
    sock = config.bind_socket()
    actual_port = sock.getsockname()[1]
    port_queue.put(actual_port)  # 把端口传出去

    # 然后用这个 socket 启动服务
    server.run(sockets=[sock])


if __name__ == "__main__":
    multiprocessing.freeze_support()

    # 创建共享队列
    win_props_queue = multiprocessing.Queue(maxsize=5)

    # 启动管理器服务
    manager = QueueManager(address=('127.0.0.1', 50000), authkey=b'abc')
    manager.register('get_win_props_queue', callable=lambda: win_props_queue)
    manager.start()
    logger.info("管理器服务已启动")

    PORT_QUEUE = multiprocessing.Queue(maxsize=3)

    # 启动 Uvicorn 服务进程
    app_process = multiprocessing.Process(target=run_app, args=(PORT_QUEUE,))
    app_process.start()

    time.sleep(0.5)

    # 等待子进程返回端口号（最多等几秒）
    try:
        actual_port = PORT_QUEUE.get(timeout=5)
        logger.info(f"Uvicorn 实际运行在端口: {actual_port}")
    except Exception as e:
        logger.info("未能获取端口号，退出:", e)
        app_process.terminate()
        sys.exit(1)

    time.sleep(0.5)

    # 启动 WebView 窗口（会阻塞直到窗口关闭）
    window = webview.create_window('Free Language Translation', f'http://127.0.0.1:{actual_port}', text_select=True)


    # 修改线程函数，使用共享队列
    def change_window_props(window: webview.Window):
        logger.info('线程中内存id: %s', id(win_props_queue))
        while APP_RUNNING:
            if not win_props_queue.empty():
                with WIN_PROPS_LOCK:
                    always_on_top = win_props_queue.get()
                    logger.info('线程中设置 on top: %s', always_on_top)
                    window.on_top = always_on_top
            time.sleep(0.5)


    change_window_thread = threading.Thread(target=change_window_props, args=(window,))
    change_window_thread.start()

    webview.start()

    # 可选：窗口关闭
    APP_RUNNING = False

    # 可选：窗口关闭后终止后台服务
    app_process.terminate()
    app_process.join()
