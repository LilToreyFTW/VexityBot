# 🖼️ VexityBot Steganography Module

This module provides advanced steganography capabilities for hiding PowerShell scripts within images and executing them on target systems.

## Features

- **Image Steganography**: Hide PowerShell scripts within PNG, JPG, JPEG, and BMP images
- **PowerShell Integration**: Generate PowerShell commands to extract and execute hidden scripts
- **GUI Interface**: User-friendly interface integrated into VexityBot
- **Batch File Generation**: Create batch files for easy execution
- **Image Validation**: Validate images for steganography compatibility
- **Size Calculation**: Calculate maximum script size that can be hidden

## Files

- `VexityBotSteganography.py` - Core steganography functionality
- `VexityBotSteganographyGUI.py` - GUI interface for steganography
- `Invoke-PixelScript.ps1` - PowerShell steganography function
- `calc.ps1` - Sample calculator script for demonstration
- `steganography_example.py` - Example usage script
- `imagecoded/momo.png` - Sample image for steganography

## Usage

### GUI Interface

1. Launch VexityBot
2. Click the "Stego" button in the toolbar
3. Use the Steganography tab to:
   - Hide scripts in images
   - Create payloads
   - Validate images
   - View PowerShell scripts

### Command Line Example

```python
from VexityBotSteganography import VexityBotSteganography

# Initialize steganography system
stego = VexityBotSteganography()

# Hide script in image
ps_command = stego.hide_script_in_image(
    script_path="calc.ps1",
    image_path="imagecoded/momo.png", 
    output_path="output.png"
)

print(ps_command)  # PowerShell execution command
```

### PowerShell Usage

```powershell
# Load the steganography function
. .\Invoke-PixelScript.ps1

# Hide script in image
Invoke-PixelScript -Script "calc.ps1" -Image "momo.png" -Out "output.png"

# The function returns a PowerShell command to extract and execute the script
```

## How It Works

1. **Script Embedding**: The script content is converted to bytes and embedded in the least significant bits of image pixels
2. **Length Storage**: The script length is stored in the first 4 pixels for proper extraction
3. **Pixel Modification**: Each byte is split across 2 pixels (4 bits per pixel) to minimize visual changes
4. **Extraction**: The PowerShell command extracts the script by reading the modified pixel values

## Security Considerations

- **Steganography Detection**: The modified images may be detectable by steganography analysis tools
- **Antivirus**: Some antivirus software may flag the generated PowerShell commands
- **Execution Policy**: PowerShell execution policy may need to be bypassed
- **Network Monitoring**: Network traffic may be monitored for suspicious activity

## Example Workflow

1. **Prepare Script**: Create or select a PowerShell script to hide
2. **Select Image**: Choose an image file (PNG recommended for best results)
3. **Hide Script**: Use the steganography function to embed the script
4. **Generate Payload**: Create PowerShell execution commands
5. **Deploy**: Place the modified image on the target system
6. **Execute**: Run the generated PowerShell command to extract and execute the script

## File Structure

```
VexityBot/
├── VexityBotSteganography.py          # Core functionality
├── VexityBotSteganographyGUI.py       # GUI interface
├── Invoke-PixelScript.ps1             # PowerShell function
├── calc.ps1                           # Sample script
├── steganography_example.py           # Example usage
├── imagecoded/
│   └── momo.png                       # Sample image
└── STEGANOGRAPHY_README.md            # This file
```

## Requirements

- Python 3.6+
- PIL (Pillow) library
- PowerShell 5.0+
- Windows OS (for PowerShell execution)

## Installation

1. Ensure all required Python packages are installed:
   ```bash
   pip install Pillow
   ```

2. Place all steganography files in the VexityBot directory

3. Launch VexityBot and access the Steganography tab

## Troubleshooting

- **Import Errors**: Ensure all files are in the correct directory
- **Image Errors**: Use supported image formats (PNG, JPG, JPEG, BMP)
- **Size Errors**: Ensure the image is large enough for the script
- **PowerShell Errors**: Check execution policy and script syntax

## Legal Notice

This tool is for educational and authorized testing purposes only. Users are responsible for complying with all applicable laws and regulations. Unauthorized use of this tool may violate local, state, or federal laws.
