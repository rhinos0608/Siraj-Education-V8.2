# SIRAJ Educational AI v8.1 - Windows PowerShell Startup Script
# Complete AI School System with Ollama + Gemma 3n
# Requires: PowerShell 5.1+ and Administrator privileges for optimal setup

param(
    [switch]$SkipGPUCheck,
    [switch]$QuickSetup,
    [switch]$BuildExe,
    [string]$DataPath = "$env:USERPROFILE\SIRAJ-Data"
)

# Color definitions for console output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Status($Message) {
    Write-ColorOutput Yellow "⏳ $Message"
}

function Write-Success($Message) {
    Write-ColorOutput Green "✅ $Message"
}

function Write-Error-Custom($Message) {
    Write-ColorOutput Red "❌ $Message"
}

function Write-Info($Message) {
    Write-ColorOutput Cyan "ℹ️  $Message"
}

# Display SIRAJ ASCII art
function Show-Banner {
    Write-ColorOutput Magenta @"
   _____ _____ _____            _    
  / ____|_   _|  __ \     /\   | |   
 | (___   | | | |__) |   /  \  | |   
  \___ \  | | |  _  /   / /\ \ | |   
  ____) |_| |_| | \ \  / ____ \| |   
 |_____/|_____|_|  \_\/_/    \_\_|   
                                     
Educational AI Council v8.1
"@

    Write-ColorOutput Cyan ""
    Write-ColorOutput Cyan "🧠 SIRAJ Educational AI v8.1 with Gemma 3n"
    Write-ColorOutput Cyan "=========================================="
    Write-Host ""
}

# Function to check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check system requirements
function Test-SystemRequirements {
    Write-Status "Checking system requirements..."
    
    # Check PowerShell version
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        Write-Error-Custom "PowerShell 5.1 or higher required. Current version: $($PSVersionTable.PSVersion)"
        exit 1
    }
    Write-Success "PowerShell version: $($PSVersionTable.PSVersion)"
    
    # Check Windows version
    $osVersion = (Get-WmiObject -Class Win32_OperatingSystem).Version
    if ([Version]$osVersion -lt [Version]"10.0") {
        Write-Error-Custom "Windows 10 or higher required for optimal Docker support"
        exit 1
    }
    Write-Success "Windows version: $osVersion"
    
    # Check memory
    $memory = [Math]::Round((Get-WmiObject -Class Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
    if ($memory -lt 8) {
        Write-Error-Custom "Insufficient memory: ${memory}GB available, 8GB required"
        Write-Info "Please upgrade your system memory for optimal AI performance"
        exit 1
    }
    Write-Success "Memory: ${memory}GB available"
    
    # Check disk space
    $freeSpace = [Math]::Round((Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace / 1GB, 1)
    if ($freeSpace -lt 20) {
        Write-Error-Custom "Insufficient disk space: ${freeSpace}GB available, 20GB required"
        Write-Info "Please free up disk space for AI models and system components"
        exit 1
    }
    Write-Success "Disk space: ${freeSpace}GB available"
    
    # Check for GPU (optional but recommended)
    if (-not $SkipGPUCheck) {
        try {
            $gpu = Get-WmiObject -Class Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" }
            if ($gpu) {
                Write-Success "NVIDIA GPU detected: $($gpu.Name) (will enable GPU acceleration)"
                $env:ENABLE_GPU = "true"
            } else {
                Write-Info "No NVIDIA GPU detected, using CPU inference (slower but functional)"
                $env:ENABLE_GPU = "false"
            }
        } catch {
            Write-Info "Could not detect GPU, continuing with CPU inference"
            $env:ENABLE_GPU = "false"
        }
    }
}

# Install Chocolatey if not present
function Install-Chocolatey {
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        Write-Status "Installing Chocolatey package manager..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Success "Chocolatey installed successfully"
    } else {
        Write-Success "Chocolatey is already installed"
    }
}

# Install Docker Desktop
function Install-Docker {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Status "Installing Docker Desktop..."
        
        if (Test-Administrator) {
            choco install docker-desktop -y
            Write-Success "Docker Desktop installed. Please restart your computer and re-run this script."
            Write-Info "After restart, make sure Docker Desktop is running before continuing."
            Read-Host "Press Enter to exit"
            exit 0
        } else {
            Write-Error-Custom "Administrator privileges required to install Docker Desktop"
            Write-Info "Please run this script as Administrator or install Docker Desktop manually"
            Write-Info "Download from: https://docs.docker.com/docker-for-windows/install/"
            exit 1
        }
    } else {
        Write-Success "Docker is installed"
    }
    
    # Check if Docker is running
    try {
        docker version | Out-Null
        Write-Success "Docker is running"
    } catch {
        Write-Error-Custom "Docker is not running. Please start Docker Desktop and try again."
        Write-Info "Look for the Docker whale icon in your system tray"
        exit 1
    }
    
    # Check Docker Compose
    try {
        docker-compose version | Out-Null
        Write-Success "Docker Compose is ready"
    } catch {
        Write-Error-Custom "Docker Compose not found. Please ensure Docker Desktop includes Docker Compose."
        exit 1
    }
}

# Install Ollama
function Install-Ollama {
    if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
        Write-Status "Installing Ollama AI engine..."
        
        # Download and install Ollama for Windows
        $ollamaInstaller = "$env:TEMP\OllamaSetup.exe"
        Write-Status "Downloading Ollama installer..."
        
        try {
            Invoke-WebRequest -Uri "https://ollama.ai/download/OllamaSetup.exe" -OutFile $ollamaInstaller
            Write-Status "Installing Ollama..."
            Start-Process -FilePath $ollamaInstaller -ArgumentList "/SILENT" -Wait
            
            # Add Ollama to PATH if not already there
            $ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama"
            if (Test-Path $ollamaPath) {
                $currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
                if ($currentPath -notlike "*$ollamaPath*") {
                    [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$ollamaPath", [EnvironmentVariableTarget]::User)
                }
            }
            
            Write-Success "Ollama installed successfully"
        } catch {
            Write-Error-Custom "Failed to download or install Ollama: $($_.Exception.Message)"
            Write-Info "Please visit https://ollama.ai and install manually"
            exit 1
        }
    } else {
        Write-Success "Ollama is already installed"
    }
    
    # Start Ollama service
    Write-Status "Starting Ollama service..."
    try {
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 5
        
        # Verify Ollama is running
        $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -TimeoutSec 10
        Write-Success "Ollama service is running"
    } catch {
        Write-Error-Custom "Failed to start Ollama service: $($_.Exception.Message)"
        exit 1
    }
}

# Setup Gemma models
function Install-GemmaModels {
    Write-Status "Setting up Gemma 3n educational models..."
    Write-Info "This may take 10-20 minutes depending on your internet connection"
    
    # Check if models are already downloaded
    try {
        $models = ollama list
        if ($models -match "gemma2:9b") {
            Write-Success "Gemma models already available"
            return
        }
    } catch {
        # Continue with download
    }
    
    Write-ColorOutput Cyan "📚 Downloading primary educational model (Gemma 2 9B)..."
    try {
        & ollama pull gemma2:9b-instruct-q4_k_m
        Write-Success "Primary model downloaded"
    } catch {
        Write-Error-Custom "Failed to download primary model: $($_.Exception.Message)"
        exit 1
    }
    
    Write-ColorOutput Cyan "📚 Downloading lightweight model (Gemma 2 2B)..."
    try {
        & ollama pull gemma2:2b-instruct-q4_k_m
        Write-Success "Lightweight model downloaded"
    } catch {
        Write-Error-Custom "Failed to download lightweight model: $($_.Exception.Message)"
        exit 1
    }
    
    # Configure educational personalities
    Write-Status "Configuring AI teaching personalities..."
    
    # Create Socratic teacher model
    $socraticModelfile = @"
FROM gemma2:9b-instruct-q4_k_m
SYSTEM """You are a Socratic teacher, one of seven AI archetypes in the SIRAJ Educational Council. 

Your role is to guide learning through strategic questions and critical thinking. Instead of giving direct answers, you ask thought-provoking questions that lead students to discover knowledge themselves.

Key principles:
- Ask "What do you think?" and "Why?" frequently
- Help students examine their assumptions
- Guide through logical reasoning steps
- Encourage intellectual curiosity
- Make thinking visible through questioning

Adapt your questioning to the grade level and subject matter. For younger students, use simpler questions. For advanced students, dive deeper into philosophical implications."""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
"@

    $socraticModelfile | Out-File -FilePath "$env:TEMP\socratic_teacher.modelfile" -Encoding UTF8
    & ollama create socratic_teacher -f "$env:TEMP\socratic_teacher.modelfile"
    
    Write-Success "Educational AI personalities configured"
}

# Setup application environment
function Initialize-Application {
    Write-Status "Setting up SIRAJ Educational AI application..."
    
    # Create data directory
    if (-not (Test-Path $DataPath)) {
        New-Item -ItemType Directory -Path $DataPath -Force | Out-Null
        Write-Success "Created data directory: $DataPath"
    }
    
    # Create environment file
    $envContent = @"
# SIRAJ Educational AI Configuration
SIRAJ_VERSION=8.1.0
SIRAJ_MODE=educational
DEPLOYMENT_TYPE=development

# AI Configuration
OLLAMA_HOST=http://localhost:11434
GEMMA_PRIMARY_MODEL=gemma2:9b-instruct-q4_k_m
GEMMA_LIGHTWEIGHT_MODEL=gemma2:2b-instruct-q4_k_m
ENABLE_GPU=$($env:ENABLE_GPU)
MAX_CONCURRENT_SESSIONS=10
TEACHING_COUNCIL_SIZE=7

# Educational Features
ADAPTIVE_LEARNING=true
MULTI_PERSPECTIVE_TEACHING=true
CURRICULUM_MAPPING=true
ASSESSMENT_GENERATION=true
LEARNING_ANALYTICS=true

# API Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=3000
API_WORKERS=2

# Database Configuration (for educational data)
POSTGRES_DB=siraj_education
POSTGRES_USER=siraj_edu
POSTGRES_PASSWORD=secure_educational_ai_2024

# Security
SECRET_KEY=$((1..64 | ForEach-Object { '{0:X}' -f (Get-Random -Max 16) }) -join '')
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Data Path
SIRAJ_DATA_PATH=$DataPath
"@

    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Success "Application environment configured"
}

# Build and start services
function Start-Services {
    Write-Status "Building and starting SIRAJ Educational services..."
    
    # Stop any existing containers
    try {
        docker-compose down 2>$null
    } catch {
        # Ignore errors if no containers are running
    }
    
    # Pull latest base images
    Write-Status "Pulling Docker base images..."
    docker-compose pull
    
    # Build and start services
    Write-Status "Building custom educational AI containers..."
    docker-compose up --build -d
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Custom "Failed to start services"
        Write-Info "Check Docker Desktop is running and try again"
        exit 1
    }
    
    Write-Success "Services started successfully"
    
    # Wait for services to be ready
    Write-Status "Waiting for services to initialize..."
    Start-Sleep -Seconds 15
    
    # Health check with retries
    $maxAttempts = 30
    $attempt = 1
    
    while ($attempt -le $maxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Success "Backend service is healthy"
                break
            }
        } catch {
            Write-Status "Attempt $attempt/$maxAttempts - waiting for backend..."
            Start-Sleep -Seconds 2
            $attempt++
        }
    }
    
    if ($attempt -gt $maxAttempts) {
        Write-Error-Custom "Backend service failed to start properly"
        Write-Info "Check logs with: docker-compose logs backend"
        exit 1
    }
    
    # Check frontend
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5
        Write-Success "Frontend service is healthy"
    } catch {
        Write-Info "Frontend may still be initializing..."
    }
}

# Build executable function
function Build-Executable {
    Show-Banner
    Write-ColorOutput Green "🔨 SIRAJ Educational AI - Executable Builder"
    Write-ColorOutput Green "==========================================="
    Write-Host ""
    
    Write-Status "Checking build prerequisites..."
    
    # Check Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Error-Custom "Python is not installed or not in PATH"
        Write-Info "Please install Python 3.11+ from https://python.org"
        exit 1
    }
    
    # Check Node.js
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
        Write-Error-Custom "Node.js is not installed or not in PATH"
        Write-Info "Please install Node.js 16+ from https://nodejs.org"
        exit 1
    }
    
    Write-Success "Build prerequisites found"
    Write-Host ""
    
    # Check if build script exists
    if (-not (Test-Path "BUILD-EXECUTABLE.bat")) {
        Write-Error-Custom "BUILD-EXECUTABLE.bat not found in current directory"
        exit 1
    }
    
    # Run the build script
    Write-Status "Starting build process..."
    & .\BUILD-EXECUTABLE.bat
}

# Display completion information
function Show-CompletionInfo {
    Write-Host ""
    Write-ColorOutput Green @"
🎓 SIRAJ Educational AI is now running!
===========================================
"@
    Write-Host ""
    
    Write-ColorOutput Cyan "📊 Educational Dashboard: http://localhost:3000"
    Write-ColorOutput Cyan "📚 API Documentation: http://localhost:8000/docs"
    Write-ColorOutput Cyan "🔍 Health Check: http://localhost:8000/health"
    Write-ColorOutput Cyan "🧠 AI Council Status: http://localhost:8000/council/status"
    Write-Host ""
    
    Write-ColorOutput Blue "🎯 What you can do now:"
    Write-Host "   • Open the dashboard and start a tutoring session"
    Write-Host "   • Submit homework for multi-perspective feedback"
    Write-Host "   • Explore curriculum-aligned learning paths"
    Write-Host "   • Watch the AI council debate educational topics"
    Write-Host ""
    
    Write-ColorOutput Yellow "📝 Useful commands:"
    Write-ColorOutput Cyan "   • View live logs: docker-compose logs -f"
    Write-ColorOutput Cyan "   • Stop system: docker-compose down"
    Write-ColorOutput Cyan "   • Restart system: docker-compose restart"
    Write-ColorOutput Cyan "   • Update models: ollama pull gemma2:9b-instruct-q4_k_m"
    Write-ColorOutput Cyan "   • Build executable: .\startup.ps1 -BuildExe"
    Write-Host ""
    
    Write-ColorOutput Magenta "🌟 Pro Tips:"
    Write-Host "   • Try asking the same question to different AI teachers"
    Write-Host "   • Upload homework assignments for detailed feedback"
    Write-Host "   • Use the curriculum overlay to align with standards"
    Write-Host "   • Check the analytics dashboard for learning insights"
    Write-Host ""
}

# Interactive menu
function Show-Menu {
    Show-Banner
    
    Write-ColorOutput Yellow "Please select an option:"
    Write-Host ""
    Write-Host "  1. Start SIRAJ Educational AI (Docker mode)"
    Write-Host "  2. Start SIRAJ Educational AI (Quick setup - skip checks)"
    Write-Host "  3. Build Standalone Executable (.exe file)"
    Write-Host "  4. Install/Update Ollama models only"
    Write-Host "  5. View application logs"
    Write-Host "  6. Stop all services"
    Write-Host "  7. Exit"
    Write-Host ""
    
    $choice = Read-Host "Enter your choice (1-7)"
    
    switch ($choice) {
        "1" {
            Main
        }
        "2" {
            $QuickSetup = $true
            Main
        }
        "3" {
            Build-Executable
        }
        "4" {
            Install-Ollama
            Install-GemmaModels
            Write-Success "Models updated successfully!"
            Read-Host "Press Enter to continue"
            Show-Menu
        }
        "5" {
            Write-ColorOutput Cyan "📊 Live Application Logs (Press Ctrl+C to exit):"
            docker-compose logs -f
            Show-Menu
        }
        "6" {
            Write-Status "Stopping all services..."
            docker-compose down
            Write-Success "All services stopped"
            Read-Host "Press Enter to continue"
            Show-Menu
        }
        "7" {
            Write-Host "Thank you for using SIRAJ Educational AI!"
            exit 0
        }
        default {
            Write-Error-Custom "Invalid choice. Please try again."
            Start-Sleep -Seconds 2
            Show-Menu
        }
    }
}

# Main execution function
function Main {
    try {
        Write-ColorOutput Magenta "🚀 Initializing SIRAJ Educational AI..."
        Write-Host ""
        
        if (-not $QuickSetup) {
            Test-SystemRequirements
            Install-Chocolatey
            Install-Docker
            Install-Ollama
            Install-GemmaModels
        }
        
        Initialize-Application
        Start-Services
        Show-CompletionInfo
        
        # Optional: show logs
        $showLogs = Read-Host "Would you like to view live application logs? (y/N)"
        if ($showLogs -eq "y" -or $showLogs -eq "Y") {
            Write-Host ""
            Write-ColorOutput Cyan "📊 Live Application Logs (Press Ctrl+C to exit):"
            docker-compose logs -f
        }
        
    } catch {
        Write-Error-Custom "An unexpected error occurred: $($_.Exception.Message)"
        Write-Info "Please check the requirements and try again"
        exit 1
    }
}

# Handle Ctrl+C gracefully
$script:CtrlCPressed = $false
[Console]::TreatControlCAsInput = $true

# Entry point
if ($BuildExe) {
    Build-Executable
} elseif ($PSBoundParameters.Count -eq 0) {
    # No parameters, show menu
    Show-Menu
} else {
    # Parameters provided, run main
    Main
}
