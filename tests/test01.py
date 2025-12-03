"""
@文件: test01.py
@作者: 雷小鸥
@日期: 2025/11/25 16:38
@许可: MIT License
@描述: 
@版本: Version 1.0
"""

import ctypes
from ctypes import wintypes, POINTER
import sys


# === 1. 定义 GUID 结构 ===
class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8)
    ]

    def __init__(self, guid_str=None):
        if guid_str:
            self.from_string(guid_str)

    def from_string(self, guid_str):
        # 移除大括号和连字符，只保留32个十六进制字符
        s = guid_str.strip('{}').replace('-', '').upper()
        if len(s) != 32:
            raise ValueError(f"Invalid GUID format: {guid_str}")
        self.Data1 = int(s[0:8], 16)
        self.Data2 = int(s[8:12], 16)
        self.Data3 = int(s[12:16], 16)
        for i in range(8):
            self.Data4[i] = int(s[16 + 2 * i: 16 + 2 * i + 2], 16)

    def __str__(self):
        return f"{{{self.Data1:08X}-{self.Data2:04X}-{self.Data3:04X}-{self.Data4[0]:02X}{self.Data4[1]:02X}-{self.Data4[2]:02X}{self.Data4[3]:02X}{self.Data4[4]:02X}{self.Data4[5]:02X}{self.Data4[6]:02X}{self.Data4[7]:02X}}}"

# 加载系统 DLL
shell32 = ctypes.windll.shell32
ole32 = ctypes.windll.ole32

# 定义 FOLDERID 常量（常用的一部分，可按需扩展）
# https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid
FOLDERID_STARTUP = GUID("{82A5EA35-D9CD-47C5-9629-E15D2F714E6E}")

# 函数声明
SHGetKnownFolderPath = shell32.SHGetKnownFolderPath
SHGetKnownFolderPath.argtypes = [
    POINTER(GUID),  # rfid
    wintypes.DWORD,  # dwFlags
    wintypes.HANDLE,  # hToken (可为 None)
    POINTER(wintypes.LPWSTR)  # ppszPath
]
SHGetKnownFolderPath.restype = ctypes.HRESULT

# CoTaskMemFree 用于释放返回的路径内存
ole32.CoTaskMemFree.argtypes = [wintypes.LPVOID]
ole32.CoTaskMemFree.restype = None


def get_known_folder_path(folder_id):
    path_ptr = wintypes.LPWSTR()
    hr = SHGetKnownFolderPath(
        ctypes.byref(folder_id),
        0,  # KF_FLAG_DEFAULT
        None,  # 当前用户
        ctypes.byref(path_ptr)
    )
    if hr != 0:
        raise OSError(f"SHGetKnownFolderPath failed with HRESULT: 0x{hr:08X}")

    try:
        return path_ptr.value
    finally:
        ole32.CoTaskMemFree(path_ptr)


if __name__ == "__main__":
    print(get_known_folder_path(FOLDERID_STARTUP))
