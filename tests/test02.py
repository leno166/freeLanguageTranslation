"""
@文件: test02.py
@作者: 雷小鸥
@日期: 2025/11/29 22:43
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
import keyboard as kb
import time
from threading import Lock, RLock

PRESSED = set()

MODE = '修改'  # 修改, 工作
MODE_RLOCK = RLock()
MODE_LOCK = Lock()


def set_mode(mode):
    global MODE
    with MODE_LOCK:
        MODE = mode


MAPPING = {
    frozenset({'=', 'ctrl'}): '增加字号',
    frozenset({'ctrl', '-'}): '减小字号',
    frozenset({'P', 'alt'}): '截图翻译',
    frozenset({'alt', 'D'}): '打开软件',
    frozenset({'alt', 'M'}): '打开mini窗口',
}
MAPPING_RLOCK = RLock()
MAPPING_LOCK = Lock()


# todo 接口, 给前端调用
def set_mapping(new_keys, action):
    global MAPPING

    with MAPPING_LOCK:
        for key, value in MAPPING:
            if value == action:
                del MAPPING[key]
                MAPPING[frozenset(sorted(set(new_keys)))] = action
                return

        raise KeyError(action)


def key_event(event):
    if event.event_type == kb.KEY_DOWN:
        PRESSED.add(event.name)

        with MODE_LOCK:
            if MODE == '修改':
                # 阻止一切按键事件
                return None

        frozen = frozenset(sorted(PRESSED))
        with MAPPING_RLOCK:
            if frozen in MAPPING.keys():
                # todo
                print(frozen)
                print(MAPPING[frozen])

                # 阻止
                return None

    else:
        with MODE_RLOCK:
            if MODE == '修改':
                # todo 一旦有抬起事件, 就要返回当前的 PRESSED, 返回给前端
                print(PRESSED)
                print(frozenset(sorted(PRESSED)))
                print()

        PRESSED.discard(event.name)

    return event


kb.hook(key_event, suppress=True)

time.sleep(100)
