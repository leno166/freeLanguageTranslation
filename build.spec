"""
@文件: free_language_translation.spec
@作者: 雷小鸥
@日期: 2025/11/24
@描述: Free Language Translation 应用打包配置
@许可: MIT License
@版本: Version 1.0
"""

block_cipher = None

a = Analysis(
    # 主脚本路径
    ['window.py'],

    # 搜索路径
    pathex=[
        '.',  # 当前目录
        './web'  # web模块目录
    ],

    # 第三方二进制依赖
    binaries=[],

    # 资源文件
    datas=[
        # UI静态资源
        ('ui', 'ui'),
    ],

    # 隐藏导入（解决打包后缺失模块的问题）
    hiddenimports=[
        'pydantic',
        'webview',
        'web',
        'modules'
    ],

    # 钩子脚本目录
    hookspath=[],

    # 钩子配置
    hooksconfig={},

    # 运行时钩子
    runtime_hooks=[],

    # 排除不需要的模块
    excludes=[],

    # 是否打包成单文件（False=目录模式）
    noarchive=False,

    # 优化级别
    optimize=1,
)

# 将纯Python代码打包成PYZ归档
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 创建可执行文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='free language translation',  # 输出可执行文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用UPX压缩
    console=False,  # note 不显示控制台窗口（GUI应用）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如需图标，可在此指定路径，如：'resource/app.ico'
)

# 如果需要创建目录分布（非单文件模式），添加COLLECT
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    a.zipped_data,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='free language translation'  # 输出目录名
)