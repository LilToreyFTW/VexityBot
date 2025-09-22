# TSM-SeniorOasisPanel Deployment Guide

## Overview
The TSM-SeniorOasisPanel is a comprehensive file transfer system with steganographic image embedding capabilities and VNC integration for remote desktop access. This guide covers the complete deployment and usage of the system.

## System Components

### Core Components
1. **TSM_SeniorOasisPanel_server.py** - Main server for file transfers and client management
2. **TSM_SeniorOasisPanel_client.py** - Client for file operations and VNC connection
3. **TSM_ImageSteganography.py** - Steganography system for hiding client in images
4. **TSM_HiddenLauncher.py** - Hidden launcher for extracting and running client from images
5. **TSM_VNCIntegration.py** - VNC integration for remote desktop access
6. **TSM_SystemTest.py** - Comprehensive testing suite

## Prerequisites

### Required Python Packages
```bash
pip install pillow
```

### System Requirements
- Python 3.7 or higher
- Windows/Linux/macOS support
- Network connectivity for client-server communication
- Sufficient disk space for file storage and temporary files

## Installation

### 1. Download and Setup
```bash
# Create project directory
mkdir TSM-SeniorOasisPanel
cd TSM-SeniorOasisPanel

# Copy all TSM files to the directory
# Ensure all Python files are in the same directory
```

### 2. Install Dependencies
```bash
pip install pillow
```

### 3. Create Server Directory
```bash
mkdir server_files
```

## Usage Guide

### 1. Starting the Server

#### Basic Server Start
```bash
python TSM_SeniorOasisPanel_server.py
```

#### Custom Configuration
The server will prompt for:
- Host address (default: localhost)
- Port number (default: 5000)

#### Server Features
- Multi-client support (up to 10 concurrent clients)
- File upload/download operations
- VNC integration support
- Comprehensive logging
- Security features (filename sanitization, file size limits)

### 2. Using the Client

#### Interactive Client
```bash
python TSM_SeniorOasisPanel_client.py
```

#### Available Commands
- `upload <filename>` - Upload a file to the server
- `download <filename>` - Download a file from the server
- `vnc` - Enable VNC screen sharing
- `exit` - Disconnect and exit

#### Hidden Mode Client
```bash
python TSM_SeniorOasisPanel_client.py --hidden
```

### 3. Steganography Operations

#### Embedding Client in Image
```bash
python TSM_ImageSteganography.py embed <original_image> <client_file> <output_image>
```

Example:
```bash
python TSM_ImageSteganography.py embed photo.jpg TSM_SeniorOasisPanel_client.py hidden_photo.png
```

#### Extracting Client from Image
```bash
python TSM_ImageSteganography.py extract <stego_image> <output_client>
```

Example:
```bash
python TSM_ImageSteganography.py extract hidden_photo.png extracted_client.py
```

#### Verifying Steganographic Image
```bash
python TSM_ImageSteganography.py verify <stego_image>
```

### 4. Hidden Deployment

#### Creating Image Viewer Launcher
```bash
python TSM_HiddenLauncher.py --create-viewer <stego_image> <viewer_output>
```

#### Launching Hidden Client
```bash
python TSM_HiddenLauncher.py --launch <stego_image> [--server host:port]
```

### 5. VNC Integration

#### Starting VNC Server
```bash
python TSM_VNCIntegration.py server [host] [port]
```

#### Starting VNC Client
```bash
python TSM_VNCIntegration.py client [host] [port]
```

## Advanced Deployment Scenarios

### Scenario 1: Hidden Client Deployment
1. Create a normal-looking image
2. Embed the client executable in the image using steganography
3. Create an image viewer launcher that appears to just view images
4. Distribute the image and launcher
5. When the image is "viewed", the hidden client connects to your server

### Scenario 2: Remote Desktop Access
1. Start the TSM server
2. Start the VNC server
3. Deploy hidden client with VNC enabled
4. Monitor and control remote desktop through the VNC connection

### Scenario 3: File Transfer Network
1. Deploy multiple TSM servers across different locations
2. Use clients to transfer files between locations
3. Implement automated file synchronization

## Security Considerations

### Server Security
- Filename sanitization prevents directory traversal attacks
- File size limits prevent memory exhaustion
- Server only accesses files in designated directory
- Comprehensive logging for audit trails

### Client Security
- Hidden mode operation for stealth deployment
- Encrypted communication protocols
- Automatic reconnection capabilities
- Clean temporary file management

### Steganography Security
- LSB (Least Significant Bit) steganography
- Data compression for efficient embedding
- Magic header verification
- Error handling for corrupted data

## Testing

### Run Complete Test Suite
```bash
python TSM_SystemTest.py
```

### Individual Component Tests
```bash
# Test server only
python -c "from TSM_SystemTest import test_server; test_server()"

# Test client only
python -c "from TSM_SystemTest import test_client; test_client()"

# Test steganography only
python -c "from TSM_SystemTest import test_steganography; test_steganography()"
```

## Troubleshooting

### Common Issues

#### Connection Refused
- Ensure server is running
- Check firewall settings
- Verify host and port configuration

#### File Upload/Download Failures
- Check file permissions
- Verify file size limits
- Ensure server_files directory exists

#### Steganography Errors
- Verify image format (PNG recommended)
- Check image size vs. data size
- Ensure image is not corrupted

#### VNC Connection Issues
- Verify VNC server is running
- Check network connectivity
- Ensure proper port configuration

### Log Files
- Server logs: `tsm_server_YYYYMMDD_HHMMSS.log`
- Client logs: Console output (or redirected to file)
- VNC logs: Console output

## Performance Optimization

### Server Optimization
- Adjust `max_clients` based on system capacity
- Modify `buffer_size` for network conditions
- Implement connection pooling for high-load scenarios

### Client Optimization
- Adjust `frame_rate` for VNC performance
- Modify `quality` setting for image compression
- Implement connection retry logic

### Steganography Optimization
- Use appropriate image sizes for data capacity
- Adjust compression levels
- Consider data chunking for large files

## Advanced Configuration

### Server Configuration
```python
server = TSMSeniorOasisPanelServer(
    host='0.0.0.0',  # Listen on all interfaces
    port=5000,       # Custom port
    max_clients=20   # Increased client limit
)
```

### Client Configuration
```python
client = TSMSeniorOasisPanelClient(
    host='your-server.com',
    port=5000
)
```

### VNC Configuration
```python
vnc = TSMVNCIntegration(
    server_host='your-vnc-server.com',
    server_port=5001
)
```

## Maintenance

### Regular Tasks
- Monitor server logs for errors
- Clean up temporary files
- Update security configurations
- Backup server_files directory

### Updates
- Test new versions in isolated environment
- Backup existing configurations
- Update client deployments
- Verify compatibility

## Support

For technical support or questions about the TSM-SeniorOasisPanel system:
1. Check the troubleshooting section
2. Review log files for error details
3. Run the system test suite
4. Verify all dependencies are installed

## License and Legal Notice

This system is provided for educational and authorized testing purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations regarding:
- Network security
- Data privacy
- Remote access permissions
- Steganography usage

Always obtain proper authorization before deploying this system in any environment.
