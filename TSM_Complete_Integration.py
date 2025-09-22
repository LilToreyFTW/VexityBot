#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Complete Integration
دمج شامل لـ noVNC و TigerVNC مع نظام TSM
"""

import os
import sys
import time
import threading
import subprocess
import webbrowser
from TSM_WebVNC import TSMWebVNCServer
from TSM_TigerVNC_Integration import TSMTigerVNCIntegration
from TSM_noVNC_Integration import TSMnoVNCServer
from TSM_PDFGenerator import TSMPDFGenerator
from TSM_PDFVNC import TSMPDFVNC, TSMPDFVNCManager

class TSMCompleteIntegration:
    """دمج شامل لجميع أنظمة VNC مع PDF-VNC Integration"""
    
    def __init__(self, host='localhost', port=8080, vnc_port=5900):
        self.host = host
        self.port = port
        self.vnc_port = vnc_port
        self.web_vnc = None
        self.tiger_vnc = None
        self.novnc = None
        self.pdf_generator = None
        self.pdf_vnc_manager = None
        self.running = False
        
    def start_all_services(self):
        """بدء جميع الخدمات مع PDF-VNC Integration"""
        print("TSM-SeniorOasisPanel: Starting Complete VNC Integration with PDF-VNC...")
        
        try:
            # بدء PDF Generator
            print("Starting PDF Generator...")
            self.pdf_generator = TSMPDFGenerator()
            print("✅ PDF Generator initialized")
            
            # بدء PDF-VNC Manager
            print("Starting PDF-VNC Manager...")
            self.pdf_vnc_manager = TSMPDFVNCManager()
            print("✅ PDF-VNC Manager initialized")
            
            time.sleep(1)
            
            # بدء TigerVNC
            print("Starting TigerVNC...")
            self.tiger_vnc = TSMTigerVNCIntegration(self.vnc_port)
            if self.tiger_vnc.start_integration():
                print("✅ TigerVNC started successfully")
            else:
                print("❌ TigerVNC failed to start")
            
            time.sleep(2)
            
            # بدء noVNC
            print("Starting noVNC...")
            self.novnc = TSMnoVNCServer(self.host, self.port, self.vnc_port)
            novnc_thread = threading.Thread(target=self.novnc.start, daemon=True)
            novnc_thread.start()
            print("✅ noVNC started successfully")
            
            time.sleep(2)
            
            # بدء Web VNC
            print("Starting Web VNC...")
            self.web_vnc = TSMWebVNCServer(self.host, self.port + 1, self.vnc_port)
            web_vnc_thread = threading.Thread(target=self.web_vnc.start, daemon=True)
            web_vnc_thread.start()
            print("✅ Web VNC started successfully")
            
            self.running = True
            print(f"\n🎯 TSM-SeniorOasisPanel Complete Integration Ready!")
            print(f"📄 PDF Generator: Ready for LaTeX generation")
            print(f"📄📺 PDF-VNC Manager: Ready for VNC embedding")
            print(f"📺 TigerVNC: localhost:{self.vnc_port}")
            print(f"🌐 noVNC Dashboard: http://{self.host}:{self.port}")
            print(f"🖥️ Web VNC: http://{self.host}:{self.port + 1}")
            print(f"\nPress Ctrl+C to stop all services...")
            
            # فتح لوحة التحكم
            webbrowser.open(f'http://{self.host}:{self.port}')
            
            # انتظار
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stop_all_services()
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Integration error: {e}")
            self.stop_all_services()
    
    def stop_all_services(self):
        """إيقاف جميع الخدمات"""
        print("\nTSM-SeniorOasisPanel: Stopping all services...")
        
        self.running = False
        
        if self.pdf_vnc_manager:
            self.pdf_vnc_manager.stop_all_vnc()
            print("✅ PDF-VNC Manager stopped")
        
        if self.tiger_vnc:
            self.tiger_vnc.stop_integration()
            print("✅ TigerVNC stopped")
        
        if self.novnc:
            self.novnc.stop()
            print("✅ noVNC stopped")
        
        if self.web_vnc:
            self.web_vnc.stop()
            print("✅ Web VNC stopped")
        
        print("🎯 TSM-SeniorOasisPanel Complete Integration stopped")
    
    def generate_pdf_with_vnc(self, code, language, output_path, vnc_config):
        """Generate PDF with VNC integration"""
        try:
            if not self.pdf_generator or not self.pdf_vnc_manager:
                return False, "PDF services not initialized"
            
            # Generate regular PDF first
            success, message = self.pdf_generator.generate_pdf_with_code(
                code, language, output_path, 
                f"TSM-SeniorOasisPanel {language} Code with VNC"
            )
            
            if not success:
                return False, f"PDF generation failed: {message}"
            
            # Embed VNC in PDF
            vnc_output_path = output_path.replace('.pdf', '_vnc.pdf')
            success, message = self.pdf_vnc_manager.process_pdf_with_vnc(
                output_path, vnc_config, vnc_output_path
            )
            
            return success, message
            
        except Exception as e:
            return False, f"PDF-VNC generation error: {str(e)}"
    
    def launch_vnc_from_pdf(self, pdf_path):
        """Launch VNC from PDF"""
        try:
            if not self.pdf_vnc_manager:
                return False, "PDF-VNC Manager not initialized"
            
            return self.pdf_vnc_manager.launch_vnc_from_pdf(pdf_path)
            
        except Exception as e:
            return False, f"VNC launch error: {str(e)}"
    
    def get_integration_status(self):
        """Get status of all integrated services"""
        status = {
            'pdf_generator': self.pdf_generator is not None,
            'pdf_vnc_manager': self.pdf_vnc_manager is not None,
            'tiger_vnc': self.tiger_vnc is not None,
            'novnc': self.novnc is not None,
            'web_vnc': self.web_vnc is not None,
            'running': self.running
        }
        return status

def main():
    """الدالة الرئيسية"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Start All: python TSM_Complete_Integration.py start [host] [port] [vnc_port]")
        print("  TigerVNC Only: python TSM_Complete_Integration.py tigervnc [port]")
        print("  noVNC Only: python TSM_Complete_Integration.py novnc [host] [port]")
        print("  Web VNC Only: python TSM_Complete_Integration.py webvnc [host] [port]")
        print("  PDF-VNC Only: python TSM_Complete_Integration.py pdfvnc [pdf_path]")
        print("  Generate PDF-VNC: python TSM_Complete_Integration.py generate [code_file] [language] [output]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'start':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        vnc_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5900
        
        integration = TSMCompleteIntegration(host, port, vnc_port)
        integration.start_all_services()
    
    elif mode == 'tigervnc':
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 5900
        tigervnc = TSMTigerVNCIntegration(port)
        try:
            if tigervnc.start_integration():
                print("TigerVNC running. Press Ctrl+C to stop.")
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            tigervnc.stop_integration()
    
    elif mode == 'novnc':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        novnc = TSMnoVNCServer(host, port)
        try:
            novnc.start()
        except KeyboardInterrupt:
            novnc.stop()
    
    elif mode == 'webvnc':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8080
        webvnc = TSMWebVNCServer(host, port)
        try:
            webvnc.start()
        except KeyboardInterrupt:
            webvnc.stop()
    
    elif mode == 'pdfvnc':
        if len(sys.argv) < 3:
            print("Usage: python TSM_Complete_Integration.py pdfvnc <pdf_path>")
            sys.exit(1)
        
        pdf_path = sys.argv[2]
        if not os.path.exists(pdf_path):
            print(f"Error: PDF file '{pdf_path}' not found")
            sys.exit(1)
        
        pdf_vnc = TSMPDFVNC()
        try:
            success, message = pdf_vnc.launch_vnc_from_pdf(pdf_path)
            print(f"TSM-SeniorOasisPanel: {message}")
            
            if success:
                print("VNC client running. Press Ctrl+C to stop.")
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            pdf_vnc.stop_vnc()
            print("VNC client stopped")
    
    elif mode == 'generate':
        if len(sys.argv) < 5:
            print("Usage: python TSM_Complete_Integration.py generate <code_file> <language> <output>")
            sys.exit(1)
        
        code_file = sys.argv[2]
        language = sys.argv[3]
        output_path = sys.argv[4]
        
        if not os.path.exists(code_file):
            print(f"Error: Code file '{code_file}' not found")
            sys.exit(1)
        
        with open(code_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # VNC configuration
        vnc_config = {
            'host': 'localhost',
            'port': 5900,
            'web_port': 8080,
            'auto_connect': True,
            'stealth_mode': True,
            'input_blocking': True,
            'screen_sharing': True,
            'file_transfer': True
        }
        
        integration = TSMCompleteIntegration()
        integration.pdf_generator = TSMPDFGenerator()
        integration.pdf_vnc_manager = TSMPDFVNCManager()
        
        success, message = integration.generate_pdf_with_vnc(code, language, output_path, vnc_config)
        print(f"TSM-SeniorOasisPanel: {message}")
    
    else:
        print("Invalid mode. Use 'start', 'tigervnc', 'novnc', 'webvnc', 'pdfvnc', or 'generate'")
        sys.exit(1)

if __name__ == "__main__":
    main()
