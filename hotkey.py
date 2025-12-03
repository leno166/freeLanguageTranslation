"""
@文件: hotkey.py
@作者: 雷小鸥
@日期: 2025/12/2 13:39
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
import keyboard as kb
from threading import Lock, RLock
from typing import TypedDict, Literal, Optional

PRESSED = set()


MAPPING: Optional[dict] = None
MAPPING_RLOCK = RLock()
MAPPING_LOCK = Lock()

def set_mapping(mapping: dict):
    global MAPPING

    with MAPPING_LOCK:
        MAPPING = mapping



def key_event(event):
    if event.event_type == kb.KEY_DOWN:
        PRESSED.add(event.name)

        frozen = frozenset(sorted(PRESSED))
        with MAPPING_RLOCK:
            if frozen in MAPPING.keys():
                # todo
                MAPPING[frozen]()
                # 阻止
                return None

    else:
        PRESSED.discard(event.name)

    return event


kb.hook(key_event, suppress=True)
