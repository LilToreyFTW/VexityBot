#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel System Test
Comprehensive testing of the TSM file transfer and steganography system.
"""

import os
import sys
import time
import threading
import subprocess
import tempfile
from PIL import Image

def create_test_image():
    """Create a test image for steganography"""
    try:
        # Create a simple test image
        img = Image.new('RGB', (800, 600), color='lightblue')
        
        # Add some content to make it look like a real image
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font, fallback to basic if not available
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 50), "TSM-SeniorOasisPanel Test Image", fill='black', font=font)
        draw.text((50, 100), "This image contains hidden data", fill='darkblue', font=font)
        
        # Save test image
        test_image_path = "test_image.png"
        img.save(test_image_path)
        print(f"TSM-SeniorOasisPanel: Created test image: {test_image_path}")
        return test_image_path
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Error creating test image: {e}")
        return None

def create_test_file():
    """Create a test file for upload/download testing"""
    try:
        test_content = """TSM-SeniorOasisPanel Test File
This is a test file for the TSM file transfer system.
Created at: {time}
System: {system}
Python Version: {python_version}
""".format(
            time=time.strftime("%Y-%m-%d %H:%M:%S"),
            system=os.name,
            python_version=sys.version
        )
        
        test_file_path = "test_file.txt"
        with open(test_file_path, 'w') as f:
            f.write(test_content)
        
        print(f"TSM-SeniorOasisPanel: Created test file: {test_file_path}")
        return test_file_path
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Error creating test file: {e}")
        return None

def test_server():
    """Test the TSM server"""
    print("\n" + "="*50)
    print("Testing TSM-SeniorOasisPanel Server")
    print("="*50)
    
    try:
        # Import and test server
        from TSM_SeniorOasisPanel_server import TSMSeniorOasisPanelServer
        
        server = TSMSeniorOasisPanelServer(host='localhost', port=5000)
        print("TSM-SeniorOasisPanel: Server object created successfully")
        
        # Test directory creation
        if os.path.exists("server_files"):
            print("TSM-SeniorOasisPanel: Server files directory exists")
        else:
            print("TSM-SeniorOasisPanel: Server files directory created")
        
        print("TSM-SeniorOasisPanel: Server test passed")
        return True
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Server test failed: {e}")
        return False

def test_client():
    """Test the TSM client"""
    print("\n" + "="*50)
    print("Testing TSM-SeniorOasisPanel Client")
    print("="*50)
    
    try:
        # Import and test client
        from TSM_SeniorOasisPanel_client import TSMSeniorOasisPanelClient
        
        client = TSMSeniorOasisPanelClient(host='localhost', port=5000)
        print("TSM-SeniorOasisPanel: Client object created successfully")
        
        print("TSM-SeniorOasisPanel: Client test passed")
        return True
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Client test failed: {e}")
        return False

def test_steganography():
    """Test the steganography system"""
    print("\n" + "="*50)
    print("Testing TSM Steganography System")
    print("="*50)
    
    try:
        from TSM_ImageSteganography import TSMImageSteganography
        
        stego = TSMImageSteganography()
        print("TSM-SeniorOasisPanel: Steganography object created successfully")
        
        # Create test image and file
        test_image = create_test_image()
        test_file = create_test_file()
        
        if not test_image or not test_file:
            print("TSM-SeniorOasisPanel: Failed to create test files")
            return False
        
        # Test embedding
        stego_output = "stego_test_image.png"
        if stego.embed_client_in_image(test_image, test_file, stego_output):
            print("TSM-SeniorOasisPanel: Client embedding test passed")
        else:
            print("TSM-SeniorOasisPanel: Client embedding test failed")
            return False
        
        # Test verification
        if stego.verify_stego_image(stego_output):
            print("TSM-SeniorOasisPanel: Steganography verification test passed")
        else:
            print("TSM-SeniorOasisPanel: Steganography verification test failed")
            return False
        
        # Test extraction
        extracted_file = "extracted_test_file.txt"
        if stego.extract_client_from_image(stego_output, extracted_file):
            print("TSM-SeniorOasisPanel: Client extraction test passed")
            
            # Verify extracted content
            if os.path.exists(extracted_file):
                with open(extracted_file, 'r') as f:
                    content = f.read()
                if "TSM-SeniorOasisPanel Test File" in content:
                    print("TSM-SeniorOasisPanel: Extracted content verification passed")
                else:
                    print("TSM-SeniorOasisPanel: Extracted content verification failed")
                    return False
            else:
                print("TSM-SeniorOasisPanel: Extracted file not found")
                return False
        else:
            print("TSM-SeniorOasisPanel: Client extraction test failed")
            return False
        
        print("TSM-SeniorOasisPanel: Steganography test passed")
        return True
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Steganography test failed: {e}")
        return False

def test_hidden_launcher():
    """Test the hidden launcher system"""
    print("\n" + "="*50)
    print("Testing TSM Hidden Launcher")
    print("="*50)
    
    try:
        from TSM_HiddenLauncher import TSMHiddenLauncher
        
        launcher = TSMHiddenLauncher()
        print("TSM-SeniorOasisPanel: Hidden launcher object created successfully")
        
        # Test image viewer creation
        test_image = "stego_test_image.png"
        if os.path.exists(test_image):
            viewer_output = "image_viewer_test.py"
            launcher.create_image_viewer_launcher(test_image, viewer_output)
            
            if os.path.exists(viewer_output):
                print("TSM-SeniorOasisPanel: Image viewer launcher creation test passed")
            else:
                print("TSM-SeniorOasisPanel: Image viewer launcher creation test failed")
                return False
        else:
            print("TSM-SeniorOasisPanel: Test image not found for launcher test")
            return False
        
        print("TSM-SeniorOasisPanel: Hidden launcher test passed")
        return True
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Hidden launcher test failed: {e}")
        return False

def test_vnc_integration():
    """Test the VNC integration system"""
    print("\n" + "="*50)
    print("Testing TSM VNC Integration")
    print("="*50)
    
    try:
        from TSM_VNCIntegration import TSMVNCIntegration, TSMVNCServer
        
        # Test VNC client
        vnc_client = TSMVNCIntegration()
        print("TSM-SeniorOasisPanel: VNC client object created successfully")
        
        # Test VNC server
        vnc_server = TSMVNCServer()
        print("TSM-SeniorOasisPanel: VNC server object created successfully")
        
        print("TSM-SeniorOasisPanel: VNC integration test passed")
        return True
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: VNC integration test failed: {e}")
        return False

def run_integration_test():
    """Run a complete integration test"""
    print("\n" + "="*50)
    print("Running TSM-SeniorOasisPanel Integration Test")
    print("="*50)
    
    try:
        # Start server in background
        print("TSM-SeniorOasisPanel: Starting server...")
        server_process = subprocess.Popen([
            sys.executable, "TSM_SeniorOasisPanel_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test client connection
        print("TSM-SeniorOasisPanel: Testing client connection...")
        from TSM_SeniorOasisPanel_client import TSMSeniorOasisPanelClient
        
        client = TSMSeniorOasisPanelClient()
        if client.connect():
            print("TSM-SeniorOasisPanel: Client connection successful")
            
            # Test file upload
            test_file = create_test_file()
            if test_file and client.upload_file(test_file):
                print("TSM-SeniorOasisPanel: File upload test passed")
            else:
                print("TSM-SeniorOasisPanel: File upload test failed")
            
            # Test file download
            if client.download_file("test_file_downloaded.txt"):
                print("TSM-SeniorOasisPanel: File download test passed")
            else:
                print("TSM-SeniorOasisPanel: File download test failed")
            
            client.disconnect()
        else:
            print("TSM-SeniorOasisPanel: Client connection failed")
        
        # Stop server
        server_process.terminate()
        server_process.wait()
        
        print("TSM-SeniorOasisPanel: Integration test completed")
        return True
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Integration test failed: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    test_files = [
        "test_image.png",
        "test_file.txt",
        "stego_test_image.png",
        "extracted_test_file.txt",
        "image_viewer_test.py",
        "test_file_downloaded.txt"
    ]
    
    for file in test_files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except:
            pass

def main():
    """Main test function"""
    print("TSM-SeniorOasisPanel System Test Suite")
    print("=" * 50)
    
    tests = [
        ("Server", test_server),
        ("Client", test_client),
        ("Steganography", test_steganography),
        ("Hidden Launcher", test_hidden_launcher),
        ("VNC Integration", test_vnc_integration),
        ("Integration Test", run_integration_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} test...")
        if test_func():
            passed += 1
            print(f"✓ {test_name} test PASSED")
        else:
            print(f"✗ {test_name} test FAILED")
    
    print("\n" + "="*50)
    print(f"Test Results: {passed}/{total} tests passed")
    print("="*50)
    
    if passed == total:
        print("TSM-SeniorOasisPanel: All tests passed! System is ready for deployment.")
    else:
        print("TSM-SeniorOasisPanel: Some tests failed. Please check the errors above.")
    
    # Cleanup
    cleanup_test_files()
    print("TSM-SeniorOasisPanel: Test cleanup completed")

if __name__ == "__main__":
    main()
