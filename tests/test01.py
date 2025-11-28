"""
@文件: test01.py
@作者: 雷小鸥
@日期: 2025/11/25 16:38
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
import webview

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            overflow: hidden;
            height: 100vh;
            background: #f0f0f0;
        }

        /* 顶部标题栏：可拖动 */
        #titlebar {
            height: 32px;
            background: #2d2d2d;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 10px;
            user-select: none;
            -webkit-app-region: drag; /* ← 关键：允许拖动（Win/macOS） */
        }

        #titlebar-buttons {
            -webkit-app-region: no-drag; /* 按钮区域不可拖 */
        }

        .btn {
            width: 30px;
            height: 24px;
            margin-left: 6px;
            background: transparent;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 12px;
        }

        .btn:hover {
            background: #555;
        }

        #content {
            padding: 20px;
            height: calc(100vh - 32px);
        }

        /* 四周拉伸区（透明，覆盖边缘） */
        .resize-handle {
            position: absolute;
            background: transparent;
            z-index: 9999;
        }
        #top, #bottom { left: 0; width: 100%; height: 6px; }
        #left, #right { top: 0; height: 100%; width: 6px; }
        #top { top: 0; cursor: ns-resize; }
        #bottom { bottom: 0; cursor: ns-resize; }
        #left { left: 0; cursor: ew-resize; }
        #right { right: 0; cursor: ew-resize; }
        #top-left { top: 0; left: 0; width: 8px; height: 8px; cursor: nw-resize; }
        #top-right { top: 0; right: 0; width: 8px; height: 8px; cursor: ne-resize; }
        #bottom-left { bottom: 0; left: 0; width: 8px; height: 8px; cursor: sw-resize; }
        #bottom-right { bottom: 0; right: 0; width: 8px; height: 8px; cursor: se-resize; }
    </style>
</head>
<body>
    <!-- 拉伸手柄 -->
    <div class="resize-handle" id="top"></div>
    <div class="resize-handle" id="bottom"></div>
    <div class="resize-handle" id="left"></div>
    <div class="resize-handle" id="right"></div>
    <div class="resize-handle" id="top-left"></div>
    <div class="resize-handle" id="top-right"></div>
    <div class="resize-handle" id="bottom-left"></div>
    <div class="resize-handle" id="bottom-right"></div>

    <!-- 标题栏 -->
    <div id="titlebar">
        <span>我的应用</span>
        <div id="titlebar-buttons">
            <button class="btn" onclick="pywebview.api.minimize()">—</button>
            <button class="btn" onclick="pywebview.api.close()">×</button>
        </div>
    </div>

    <div id="content">
        <h2>无边框窗口 + 拖拽 + 拉伸</h2>
        <p>尝试拖动顶部移动窗口，或拖动边缘/角落调整大小。</p>
    </div>

    <script>
        // 边缘拉伸逻辑
        const handles = [
            'top', 'bottom', 'left', 'right',
            'top-left', 'top-right', 'bottom-left', 'bottom-right'
        ];

        let isResizing = false;
        let currentHandle = null;
        let startX, startY, startWidth, startHeight, startLeft, startTop;

        function setupResize(handleId) {
            const el = document.getElementById(handleId);
            el.addEventListener('mousedown', (e) => {
                isResizing = true;
                currentHandle = handleId;
                startX = e.screenX;
                startY = e.screenY;

                const rect = pywebview.api.getWindowRect();
                startWidth = rect.width;
                startHeight = rect.height;
                startLeft = rect.x;
                startTop = rect.y;

                e.preventDefault();
                document.body.style.cursor = getComputedStyle(el).cursor;
                document.addEventListener('mousemove', doResize);
                document.addEventListener('mouseup', stopResize);
            });
        }

        function doResize(e) {
            if (!isResizing) return;
            const dx = e.screenX - startX;
            const dy = e.screenY - startY;

            let newWidth = startWidth;
            let newHeight = startHeight;
            let newLeft = startLeft;
            let newTop = startTop;

            if (currentHandle.includes('right')) {
                newWidth = Math.max(200, startWidth + dx);
            }
            if (currentHandle.includes('left')) {
                newWidth = Math.max(200, startWidth - dx);
                newLeft = startLeft + (startWidth - newWidth);
            }
            if (currentHandle.includes('bottom')) {
                newHeight = Math.max(150, startHeight + dy);
            }
            if (currentHandle.includes('top')) {
                newHeight = Math.max(150, startHeight - dy);
                newTop = startTop + (startHeight - newHeight);
            }

            pywebview.api.resize(newWidth, newHeight, newLeft, newTop);
        }

        function stopResize() {
            isResizing = false;
            currentHandle = null;
            document.body.style.cursor = '';
            document.removeEventListener('mousemove', doResize);
            document.removeEventListener('mouseup', stopResize);
        }

        // 初始化所有拉伸手柄
        handles.forEach(setupResize);
    </script>
</body>
</html>
"""


class Api:
    def __init__(self):
        self.window = None

    def set_window(self, window):
        self.window = window

    def close(self):
        if self.window:
            self.window.destroy()

    def minimize(self):
        if self.window:
            self.window.minimize()

    def getWindowRect(self):
        """返回当前窗口位置和尺寸"""
        if self.window:
            return {
                "x": self.window.x,
                "y": self.window.y,
                "width": self.window.width,
                "height": self.window.height,
            }
        return {"x": 0, "y": 0, "width": 800, "height": 600}

    def resize(self, width, height, x, y):
        if self.window:
            # 注意：pywebview 的 resize 是 (width, height)，move 是 (x, y)
            self.window.resize(width, height)
            self.window.move(x, y)


if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        title='Resizable Frameless App',
        html=html,
        js_api=api,
        frameless=True,
        width=800,
        height=600,
        easy_drag=False  # 必须设为 False，否则会干扰自定义拖动
    )
    api.set_window(window)
    webview.start(debug=True)
