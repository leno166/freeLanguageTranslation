"""
@文件: window.py
@作者: 雷小鸥
@日期: 2025/11/24 12:59
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
from typing import Optional
import webview
import sys
from pathlib import Path
import winshell
from logger import logger
from web.languageTranslations import deepseek
from modules.infi.systray import SysTrayIcon
from threading import Lock
from pprint import pprint
from hotkey import set_mapping
import time

SYSTRAY: Optional[SysTrayIcon] = None
WINDOW: Optional[webview.Window] = None

BASE_PATH: Optional[Path] = None
EXE_PATH: Optional[Path] = None
try:
    BASE_PATH = Path(sys._MEIPASS)
    EXE_PATH = Path(sys.executable)
except Exception:
    BASE_PATH = Path(__file__).parent
    EXE_PATH = Path(sys.executable)

APP_NAME = 'Free Language Translation'

SYSTRAY_RUNNING: bool = True
SYSTRAY_RUNNING_LOCK: Lock = Lock()


def open_main_windows(systray: Optional[SysTrayIcon] = None) -> None:
    WINDOW.show()
    WINDOW.restore()


def open_setting(systray: Optional[SysTrayIcon] = None) -> None:
    WINDOW.show()
    WINDOW.restore()


def on_systray_quit(systray: Optional[SysTrayIcon]):
    global SYSTRAY_RUNNING
    with SYSTRAY_RUNNING_LOCK:
        SYSTRAY_RUNNING = False
    WINDOW.destroy()


def on_window_quit():
    print('on_window_quit')
    WINDOW.hide()
    if SYSTRAY_RUNNING:
        return False


class Api:
    _always_on_top_lock = Lock()

    # ====================================================
    # 翻译
    # ====================================================

    # ====================================================
    # 选择语言
    def change_language(self, language: str):
        pass

    # ====================================================
    # 翻译
    def translation(self, text: str):
        logger.info('待翻译文本: %s', text)
        translator = deepseek.get(text)
        logger.info("翻译文本: %s", translator)
        return translator

    # ====================================================
    # 设置
    # ====================================================

    # 配置更新
    def config_update(self, configs: dict):
        pprint(configs)

        self.set_auto_running(configs['autoStart'])
        self.set_hide2tray_on_start(configs['startMinimized'])

        self.set_always_on_top(configs['alwaysOnTop'])
        self.set_hide2tray_on_close(configs['hide2trayOnClose'])

    # ====================================================
    # 启动
    def set_auto_running(self, enable: bool):
        # todo: 通过创建, 删除 快捷图标的方式实现自启动和取消自启动
        startup_dir = (
                Path('~').expanduser()
                / 'AppData' / 'Roaming' / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
        )

        shortcut_path = startup_dir / f'{APP_NAME}.lnk'

        if enable:
            if shortcut_path.exists():
                shortcut_path.unlink()

            winshell.CreateShortcut(
                Path=str(shortcut_path),
                Target=str(EXE_PATH),
                Icon=(sys.executable, 0),
                Description='Auto Start Free Language Translation'
            )

        else:
            if shortcut_path.exists():
                shortcut_path.unlink()  # 删除快捷方式

    def set_hide2tray_on_start(self, enable: bool):
        print('set_hide2tray_on_start: ', enable)

        if enable:
            WINDOW.hide()

    # ====================================================
    # 快捷键
    def modify_hotkey(self, item: dict):
        return item

    # ====================================================
    # 主窗口
    def set_always_on_top(self, enable: bool):
        logger.info(enable)
        with self._always_on_top_lock:
            WINDOW.on_top = enable

    def set_hide2tray_on_close(self, enable: bool):
        if enable:
            try:
                WINDOW.events.closing -= on_window_quit
            except ValueError as e:
                print('注册前先尝试移除, 异常: ', e)

            WINDOW.events.closing += on_window_quit
        else:
            try:
                WINDOW.events.closing -= on_window_quit
            except ValueError as e:
                print('未注册 on_window_quit: ', e)

    # ====================================================
    # 截屏翻译
    def capture_single(self):
        pass

    def capture_all(self):
        pass


# =====================================================
# 后端调用: window.api.xxx
# =====================================================
def increase_font_size():
    WINDOW.run_js('window.api.increaseFontSize()')


def decrease_font_size():
    WINDOW.run_js('window.api.decreaseFontSize()')


# =====================================================
# 给 hotkey 的回调函数
# =====================================================
set_mapping({
    frozenset({'=', 'ctrl'}): increase_font_size,  # '增加字号'
    frozenset({'ctrl', '-'}): decrease_font_size,  # '减小字号'
    frozenset({'P', 'alt'}): '截图翻译',
    frozenset({'alt', 'D'}): '打开软件',
    frozenset({'alt', 'M'}): '打开mini窗口',
})

if __name__ == "__main__":
    # 启动 WebView 窗口（会阻塞直到窗口关闭）
    WINDOW = webview.create_window(
        'Free Language Translation', str(BASE_PATH / 'ui/index.html'), js_api=Api(),
        text_select=True
    )

    # 系统托盘
    with SysTrayIcon(
            icon=None, hover_text='Free Language Translation', on_quit=on_systray_quit,
            menu_options=(
                    ('打开主界面', None, open_main_windows), ('设置', None, open_setting),
            ), default_menu_index=0,
    ) as SYSTRAY:
        # WINDOW.events.closing += on_window_quit

        # todo 做之前, 需要加载前端存储的配置表, 检查是否需要这个.

        webview.start(private_mode=False, debug=False)
