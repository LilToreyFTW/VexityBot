# ADDED - Sample PowerShell script for steganography demonstration
# This is a simple calculator script that can be hidden in images

Write-Host "VexityBot Steganography Demo - Calculator" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Simple calculator function
function Show-Calculator {
    Write-Host "`nAvailable Operations:" -ForegroundColor Yellow
    Write-Host "1. Addition (+)"
    Write-Host "2. Subtraction (-)"
    Write-Host "3. Multiplication (*)"
    Write-Host "4. Division (/)"
    Write-Host "5. Exit"
    
    $choice = Read-Host "`nSelect operation (1-5)"
    
    switch ($choice) {
        "1" { 
            $num1 = [double](Read-Host "Enter first number")
            $num2 = [double](Read-Host "Enter second number")
            $result = $num1 + $num2
            Write-Host "Result: $num1 + $num2 = $result" -ForegroundColor Cyan
        }
        "2" { 
            $num1 = [double](Read-Host "Enter first number")
            $num2 = [double](Read-Host "Enter second number")
            $result = $num1 - $num2
            Write-Host "Result: $num1 - $num2 = $result" -ForegroundColor Cyan
        }
        "3" { 
            $num1 = [double](Read-Host "Enter first number")
            $num2 = [double](Read-Host "Enter second number")
            $result = $num1 * $num2
            Write-Host "Result: $num1 * $num2 = $result" -ForegroundColor Cyan
        }
        "4" { 
            $num1 = [double](Read-Host "Enter first number")
            $num2 = [double](Read-Host "Enter second number")
            if ($num2 -eq 0) {
                Write-Host "Error: Division by zero!" -ForegroundColor Red
            } else {
                $result = $num1 / $num2
                Write-Host "Result: $num1 / $num2 = $result" -ForegroundColor Cyan
            }
        }
        "5" { 
            Write-Host "Exiting calculator..." -ForegroundColor Yellow
            return $false
        }
        default { 
            Write-Host "Invalid choice! Please select 1-5." -ForegroundColor Red
        }
    }
    return $true
}

# Main calculator loop
do {
    $continue = Show-Calculator
} while ($continue)

Write-Host "`nCalculator session ended." -ForegroundColor Green
