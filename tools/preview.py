#!/usr/bin/env python3
"""本地预览服务器（带 no-cache）。

为什么不用 `python3 -m http.server`：它不发 Cache-Control、只发 Last-Modified，
浏览器会按 mtime 做**启发式缓存** —— 改完 HTML 刷新可能还是旧的，
就会出现「旧 HTML + 新 script.js」的版本错配（曾经导致页面报
`Cannot set properties of null`，还伪装成"加载失败"）。

用法：
    python3 tools/preview.py          # 默认 8899
    python3 tools/preview.py 8902     # 指定端口

根目录固定为 ../web（相对本脚本）。"""
import functools
import http.server
import os
import sys


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def send_header(self, key, value):
        # 去掉 Last-Modified，浏览器就无从做启发式缓存
        if key.lower() == "last-modified":
            return
        super().send_header(key, value)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # 静默：预览时的请求日志没有价值，别刷屏


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8899
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web")
    handler = functools.partial(NoCacheHandler, directory=root)
    print(f"预览：http://127.0.0.1:{port}/  （no-cache，改完直接刷新即见）", flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()


if __name__ == "__main__":
    main()
