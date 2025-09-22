#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel noVNC Integration
دمج noVNC مع نظام TSM للتحكم عبر المتصفح
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

class TSMnoVNCHandler(BaseHTTPRequestHandler):
    """معالج HTTP لـ TSM noVNC"""
    
    def __init__(self, novnc_server, *args, **kwargs):
        self.novnc_server = novnc_server
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """معالجة طلبات GET"""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/':
                self.serve_tsm_dashboard()
            elif path == '/vnc.html':
                self.serve_novnc_page()
            elif path == '/vnc_lite.html':
                self.serve_novnc_lite()
            elif path == '/websockify':
                self.handle_websocket_proxy()
            elif path.startswith('/app/'):
                self.serve_novnc_app(path)
            elif path.startswith('/core/'):
                self.serve_novnc_core(path)
            elif path.startswith('/vendor/'):
                self.serve_novnc_vendor(path)
            elif path == '/api/status':
                self.serve_api_status()
            elif path == '/api/screenshot':
                self.serve_api_screenshot()
            else:
                self.send_error(404, "File not found")
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: noVNC handler error: {e}")
            self.send_error(500, "Internal server error")
    
    def serve_tsm_dashboard(self):
        """خدمة لوحة تحكم TSM"""
        html_content = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TSM-SeniorOasisPanel Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header p {
            font-size: 1.3em;
            opacity: 0.9;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .dashboard-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        }
        
        .card-title {
            font-size: 1.5em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .card-content {
            margin-bottom: 20px;
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
            text-decoration: none;
            display: inline-block;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        .btn-secondary {
            background: linear-gradient(45deg, #4ecdc4, #44a08d);
        }
        
        .btn-success {
            background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online { background: #2ecc71; }
        .status-offline { background: #e74c3c; }
        .status-connecting { background: #f39c12; }
        
        .vnc-container {
            grid-column: 1 / -1;
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
        }
        
        #vnc-screen {
            width: 100%;
            height: 600px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 10px;
            background: #000;
        }
        
        .controls {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
            justify-content: center;
        }
        
        .info-panel {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .info-item:last-child {
            border-bottom: none;
        }
        
        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .controls {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 TSM-SeniorOasisPanel</h1>
            <p>نظام التحكم عن بُعد المخفي المتقدم | Advanced Hidden Remote Control System</p>
        </div>
        
        <div class="dashboard-grid">
            <div class="dashboard-card">
                <div class="card-title">
                    <span class="status-indicator status-offline" id="server-status"></span>
                    🖥️ حالة الخادم | Server Status
                </div>
                <div class="card-content">
                    <div class="info-panel">
                        <div class="info-item">
                            <span>الخادم | Server:</span>
                            <span id="server-address">localhost:5000</span>
                        </div>
                        <div class="info-item">
                            <span>الحالة | Status:</span>
                            <span id="server-status-text">غير متصل | Offline</span>
                        </div>
                        <div class="info-item">
                            <span>العملاء المتصلون | Connected Clients:</span>
                            <span id="connected-clients">0</span>
                        </div>
                    </div>
                </div>
                <button class="btn" onclick="connectServer()">🔗 الاتصال | Connect</button>
                <button class="btn btn-secondary" onclick="disconnectServer()">❌ قطع الاتصال | Disconnect</button>
            </div>
            
            <div class="dashboard-card">
                <div class="card-title">
                    <span class="status-indicator status-offline" id="vnc-status"></span>
                    📺 VNC Control
                </div>
                <div class="card-content">
                    <div class="info-panel">
                        <div class="info-item">
                            <span>VNC Server:</span>
                            <span id="vnc-address">localhost:5900</span>
                        </div>
                        <div class="info-item">
                            <span>الحالة | Status:</span>
                            <span id="vnc-status-text">غير متصل | Offline</span>
                        </div>
                        <div class="info-item">
                            <span>الجودة | Quality:</span>
                            <span id="vnc-quality">90%</span>
                        </div>
                    </div>
                </div>
                <button class="btn btn-success" onclick="startVNC()">🚀 بدء VNC | Start VNC</button>
                <button class="btn" onclick="openVNC()">🌐 فتح VNC | Open VNC</button>
            </div>
            
            <div class="dashboard-card">
                <div class="card-title">
                    📁 إدارة الملفات | File Management
                </div>
                <div class="card-content">
                    <div class="info-panel">
                        <div class="info-item">
                            <span>الملفات المحملة | Uploaded Files:</span>
                            <span id="uploaded-files">0</span>
                        </div>
                        <div class="info-item">
                            <span>الملفات المحملة | Downloaded Files:</span>
                            <span id="downloaded-files">0</span>
                        </div>
                        <div class="info-item">
                            <span>المساحة المستخدمة | Used Space:</span>
                            <span id="used-space">0 MB</span>
                        </div>
                    </div>
                </div>
                <button class="btn" onclick="uploadFile()">📤 رفع ملف | Upload File</button>
                <button class="btn btn-secondary" onclick="downloadFile()">📥 تحميل ملف | Download File</button>
            </div>
            
            <div class="dashboard-card">
                <div class="card-title">
                    🔒 الأمان والخفاء | Security & Stealth
                </div>
                <div class="card-content">
                    <div class="info-panel">
                        <div class="info-item">
                            <span>الوضع المخفي | Stealth Mode:</span>
                            <span id="stealth-status">نشط | Active</span>
                        </div>
                        <div class="info-item">
                            <span>حجب الإدخالات | Input Blocking:</span>
                            <span id="input-blocking">غير نشط | Inactive</span>
                        </div>
                        <div class="info-item">
                            <span>التشفير | Encryption:</span>
                            <span id="encryption-status">نشط | Active</span>
                        </div>
                    </div>
                </div>
                <button class="btn" onclick="toggleStealth()">👻 تبديل الخفاء | Toggle Stealth</button>
                <button class="btn btn-secondary" onclick="toggleInputBlocking()">🚫 حجب الإدخالات | Block Input</button>
            </div>
        </div>
        
        <div class="vnc-container">
            <div class="card-title">
                📺 شاشة التحكم | Control Screen
            </div>
            <div class="controls">
                <button class="btn" onclick="connectVNC()">🔗 الاتصال بـ VNC | Connect VNC</button>
                <button class="btn btn-secondary" onclick="disconnectVNC()">❌ قطع VNC | Disconnect VNC</button>
                <button class="btn" onclick="toggleFullscreen()">📺 ملء الشاشة | Fullscreen</button>
                <button class="btn" onclick="takeScreenshot()">📸 لقطة شاشة | Screenshot</button>
                <button class="btn" onclick="sendCtrlAltDel()">⌨️ Ctrl+Alt+Del</button>
            </div>
            <canvas id="vnc-screen"></canvas>
        </div>
    </div>
    
    <script>
        // متغيرات النظام
        let serverConnected = false;
        let vncConnected = false;
        let vncClient = null;
        let statusInterval = null;
        
        // بدء مراقبة الحالة
        function startStatusMonitoring() {
            statusInterval = setInterval(updateStatus, 2000);
        }
        
        // تحديث حالة النظام
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    updateServerStatus(data.server);
                    updateVNCStatus(data.vnc);
                    updateFileStatus(data.files);
                    updateSecurityStatus(data.security);
                })
                .catch(error => {
                    console.error('Status update error:', error);
                });
        }
        
        // تحديث حالة الخادم
        function updateServerStatus(serverData) {
            const statusIndicator = document.getElementById('server-status');
            const statusText = document.getElementById('server-status-text');
            const connectedClients = document.getElementById('connected-clients');
            
            if (serverData.connected) {
                statusIndicator.className = 'status-indicator status-online';
                statusText.textContent = 'متصل | Online';
                connectedClients.textContent = serverData.clients || 0;
                serverConnected = true;
            } else {
                statusIndicator.className = 'status-indicator status-offline';
                statusText.textContent = 'غير متصل | Offline';
                connectedClients.textContent = '0';
                serverConnected = false;
            }
        }
        
        // تحديث حالة VNC
        function updateVNCStatus(vncData) {
            const statusIndicator = document.getElementById('vnc-status');
            const statusText = document.getElementById('vnc-status-text');
            const quality = document.getElementById('vnc-quality');
            
            if (vncData.connected) {
                statusIndicator.className = 'status-indicator status-online';
                statusText.textContent = 'متصل | Online';
                quality.textContent = vncData.quality + '%';
                vncConnected = true;
            } else {
                statusIndicator.className = 'status-indicator status-offline';
                statusText.textContent = 'غير متصل | Offline';
                quality.textContent = '0%';
                vncConnected = false;
            }
        }
        
        // تحديث حالة الملفات
        function updateFileStatus(fileData) {
            document.getElementById('uploaded-files').textContent = fileData.uploaded || 0;
            document.getElementById('downloaded-files').textContent = fileData.downloaded || 0;
            document.getElementById('used-space').textContent = fileData.usedSpace || '0 MB';
        }
        
        // تحديث حالة الأمان
        function updateSecurityStatus(securityData) {
            document.getElementById('stealth-status').textContent = 
                securityData.stealth ? 'نشط | Active' : 'غير نشط | Inactive';
            document.getElementById('input-blocking').textContent = 
                securityData.inputBlocking ? 'نشط | Active' : 'غير نشط | Inactive';
            document.getElementById('encryption-status').textContent = 
                securityData.encryption ? 'نشط | Active' : 'غير نشط | Inactive';
        }
        
        // الاتصال بالخادم
        function connectServer() {
            fetch('/api/connect', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('Server connected');
                    } else {
                        console.error('Server connection failed:', data.error);
                    }
                })
                .catch(error => {
                    console.error('Server connection error:', error);
                });
        }
        
        // قطع الاتصال بالخادم
        function disconnectServer() {
            fetch('/api/disconnect', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('Server disconnected');
                    }
                })
                .catch(error => {
                    console.error('Server disconnection error:', error);
                });
        }
        
        // بدء VNC
        function startVNC() {
            fetch('/api/start-vnc', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('VNC started');
                    } else {
                        console.error('VNC start failed:', data.error);
                    }
                })
                .catch(error => {
                    console.error('VNC start error:', error);
                });
        }
        
        // فتح VNC
        function openVNC() {
            window.open('/vnc.html', '_blank');
        }
        
        // الاتصال بـ VNC
        function connectVNC() {
            if (!vncConnected) {
                vncClient = new WebSocket('ws://localhost:6080/websockify');
                
                vncClient.onopen = function() {
                    vncConnected = true;
                    console.log('VNC Connected');
                };
                
                vncClient.onmessage = function(event) {
                    handleVNCData(event.data);
                };
                
                vncClient.onclose = function() {
                    vncConnected = false;
                    console.log('VNC Disconnected');
                };
                
                vncClient.onerror = function(error) {
                    console.error('VNC Error:', error);
                };
            }
        }
        
        // قطع الاتصال بـ VNC
        function disconnectVNC() {
            if (vncClient && vncConnected) {
                vncClient.close();
            }
        }
        
        // معالجة بيانات VNC
        function handleVNCData(data) {
            const canvas = document.getElementById('vnc-screen');
            const ctx = canvas.getContext('2d');
            
            // معالجة بيانات VNC وعرضها
            // This is where VNC data processing and display will happen
        }
        
        // ملء الشاشة
        function toggleFullscreen() {
            const container = document.querySelector('.vnc-container');
            if (!document.fullscreenElement) {
                container.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        }
        
        // لقطة شاشة
        function takeScreenshot() {
            fetch('/api/screenshot')
                .then(response => response.blob())
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'tsm-screenshot-' + Date.now() + '.png';
                    a.click();
                    URL.revokeObjectURL(url);
                })
                .catch(error => {
                    console.error('Screenshot error:', error);
                });
        }
        
        // إرسال Ctrl+Alt+Del
        function sendCtrlAltDel() {
            if (vncClient && vncConnected) {
                // إرسال Ctrl+Alt+Del عبر VNC
                const ctrlAltDel = new Uint8Array([0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]);
                vncClient.send(ctrlAltDel);
            }
        }
        
        // تبديل الوضع المخفي
        function toggleStealth() {
            fetch('/api/toggle-stealth', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    console.log('Stealth mode toggled:', data.stealth);
                })
                .catch(error => {
                    console.error('Stealth toggle error:', error);
                });
        }
        
        // تبديل حجب الإدخالات
        function toggleInputBlocking() {
            fetch('/api/toggle-input-blocking', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    console.log('Input blocking toggled:', data.blocking);
                })
                .catch(error => {
                    console.error('Input blocking toggle error:', error);
                });
        }
        
        // رفع ملف
        function uploadFile() {
            const input = document.createElement('input');
            input.type = 'file';
            input.onchange = function(e) {
                const file = e.target.files[0];
                if (file) {
                    const formData = new FormData();
                    formData.append('file', file);
                    
                    fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log('File uploaded successfully');
                        } else {
                            console.error('File upload failed:', data.error);
                        }
                    })
                    .catch(error => {
                        console.error('File upload error:', error);
                    });
                }
            };
            input.click();
        }
        
        // تحميل ملف
        function downloadFile() {
            const filename = prompt('Enter filename to download:');
            if (filename) {
                fetch(`/api/download/${filename}`)
                    .then(response => response.blob())
                    .then(blob => {
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = filename;
                        a.click();
                        URL.revokeObjectURL(url);
                    })
                    .catch(error => {
                        console.error('File download error:', error);
                    });
            }
        }
        
        // بدء النظام
        window.onload = function() {
            startStatusMonitoring();
            console.log('TSM-SeniorOasisPanel Dashboard loaded');
        };
    </script>
</body>
</html>
"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_novnc_page(self):
        """خدمة صفحة noVNC"""
        novnc_path = os.path.join('noVNC', 'vnc.html')
        if os.path.exists(novnc_path):
            with open(novnc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # تخصيص noVNC لـ TSM
            content = content.replace(
                '<title>noVNC</title>',
                '<title>TSM-SeniorOasisPanel VNC</title>'
            )
            
            # إضافة معلومات TSM
            tsm_info = '''
            <script>
                // TSM-SeniorOasisPanel Integration
                window.TSM_CONFIG = {
                    server: 'localhost:5000',
                    vnc_port: 5900,
                    stealth_mode: true,
                    auto_connect: true
                };
            </script>
            '''
            
            content = content.replace('</head>', tsm_info + '</head>')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_error(404, "noVNC not found")
    
    def serve_novnc_lite(self):
        """خدمة noVNC Lite"""
        novnc_lite_path = os.path.join('noVNC', 'vnc_lite.html')
        if os.path.exists(novnc_lite_path):
            with open(novnc_lite_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_error(404, "noVNC Lite not found")
    
    def serve_novnc_app(self, path):
        """خدمة ملفات noVNC app"""
        file_path = os.path.join('noVNC', path[1:])
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # تحديد نوع المحتوى
            if file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File not found")
    
    def serve_novnc_core(self, path):
        """خدمة ملفات noVNC core"""
        file_path = os.path.join('noVNC', path[1:])
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            
            content_type = 'application/javascript' if file_path.endswith('.js') else 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File not found")
    
    def serve_novnc_vendor(self, path):
        """خدمة ملفات noVNC vendor"""
        file_path = os.path.join('noVNC', path[1:])
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            
            content_type = 'application/javascript' if file_path.endswith('.js') else 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File not found")
    
    def serve_api_status(self):
        """خدمة API للحالة"""
        try:
            status_data = {
                'server': {
                    'connected': True,
                    'clients': 1,
                    'port': 5000
                },
                'vnc': {
                    'connected': True,
                    'quality': 90,
                    'port': 5900
                },
                'files': {
                    'uploaded': 5,
                    'downloaded': 3,
                    'usedSpace': '25 MB'
                },
                'security': {
                    'stealth': True,
                    'inputBlocking': False,
                    'encryption': True
                }
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status_data).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Status API error: {e}")
    
    def serve_api_screenshot(self):
        """خدمة API للقطة الشاشة"""
        try:
            # التقاط لقطة شاشة
            screenshot = ImageGrab.grab()
            
            # تحويل إلى PNG
            output = io.BytesIO()
            screenshot.save(output, format='PNG')
            screenshot_data = output.getvalue()
            
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.send_header('Content-Length', str(len(screenshot_data)))
            self.end_headers()
            self.wfile.write(screenshot_data)
            
        except Exception as e:
            self.send_error(500, f"Screenshot API error: {e}")
    
    def handle_websocket_proxy(self):
        """معالجة WebSocket proxy"""
        # هذا سيتم تنفيذه مع websockify
        self.send_error(501, "WebSocket proxy not implemented yet")
    
    def log_message(self, format, *args):
        """تسجيل رسائل HTTP"""
        print(f"TSM-SeniorOasisPanel: {format % args}")

class TSMnoVNCServer:
    """خادم noVNC لـ TSM"""
    
    def __init__(self, host='localhost', port=8080, vnc_port=5900):
        self.host = host
        self.port = port
        self.vnc_port = vnc_port
        self.http_server = None
        self.websockify_process = None
        self.running = False
        
    def start_websockify(self):
        """بدء websockify"""
        try:
            websockify_path = os.path.join('noVNC', 'utils', 'websockify', 'websockify.py')
            
            if os.path.exists(websockify_path):
                cmd = [
                    sys.executable, websockify_path,
                    '6080', f'localhost:{self.vnc_port}',
                    '--web', 'noVNC'
                ]
                self.websockify_process = subprocess.Popen(cmd)
                print("TSM-SeniorOasisPanel: WebSockify started on port 6080")
                return True
            else:
                print("TSM-SeniorOasisPanel: WebSockify not found")
                return False
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: WebSockify error: {e}")
            return False
    
    def start_http_server(self):
        """بدء خادم HTTP"""
        try:
            def handler(*args, **kwargs):
                return TSMnoVNCHandler(self, *args, **kwargs)
            
            self.http_server = HTTPServer((self.host, self.port), handler)
            self.running = True
            
            print(f"TSM-SeniorOasisPanel: noVNC Server started on http://{self.host}:{self.port}")
            
            # فتح المتصفح تلقائياً
            webbrowser.open(f'http://{self.host}:{self.port}')
            
            self.http_server.serve_forever()
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: noVNC Server error: {e}")
    
    def start(self):
        """بدء جميع الخدمات"""
        print("TSM-SeniorOasisPanel: Starting noVNC System...")
        
        # بدء websockify
        if self.start_websockify():
            time.sleep(2)
            
            # بدء خادم HTTP
            self.start_http_server()
        else:
            print("TSM-SeniorOasisPanel: Failed to start WebSockify")
    
    def stop(self):
        """إيقاف جميع الخدمات"""
        self.running = False
        
        if self.websockify_process:
            self.websockify_process.terminate()
        
        if self.http_server:
            self.http_server.shutdown()
        
        print("TSM-SeniorOasisPanel: noVNC System stopped")

def main():
    """الدالة الرئيسية"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Server: python TSM_noVNC_Integration.py server [host] [port] [vnc_port]")
        print("  Dashboard: python TSM_noVNC_Integration.py dashboard [host] [port]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'server':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        vnc_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5900
        
        server = TSMnoVNCServer(host=host, port=port, vnc_port=vnc_port)
        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()
    
    elif mode == 'dashboard':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        
        webbrowser.open(f'http://{host}:{port}')
        print(f"TSM-SeniorOasisPanel: Dashboard opened at http://{host}:{port}")
    
    else:
        print("Invalid mode. Use 'server' or 'dashboard'")
        sys.exit(1)

if __name__ == "__main__":
    main()
