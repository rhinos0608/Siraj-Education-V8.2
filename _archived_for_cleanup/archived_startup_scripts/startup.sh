#!/bin/bash

# SIRAJ Educational AI v8.1 - Unix Bash Startup Script
# Complete AI School System with Ollama + Gemma 3n

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ASCII Art for SIRAJ
printf "${PURPLE}"
cat << "EOF"
   _____ _____ _____            _    
  / ____|_   _|  __ \     /\   | |   
 | (___   | | | |__) |   /  \  | |   
  \___ \  | | |  _  /   / /\ \ | |   
  ____) |_| |_| | \ \  / ____ \| |   
 |_____/|_____|_|  \_\/_/    \_\_|   
                                     
Educational AI Council v8.1
EOF
printf "${NC}\n"

printf "${CYAN}🧠 Starting SIRAJ Educational AI v8.1 with Gemma 3n${NC}\n"
printf "${CYAN}=================================================${NC}\n\n"

# Function to print status messages
print_status() {
    printf "${YELLOW}⏳ $1${NC}\n"
}

print_success() {
    printf "${GREEN}✅ $1${NC}\n"
}

print_error() {
    printf "${RED}❌ $1${NC}\n"
}

print_info() {
    printf "${BLUE}ℹ️  $1${NC}\n"
}

# Check system requirements
check_system_requirements() {
    print_status "Checking system requirements..."
    
    # Check OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        print_success "Operating System: Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        print_success "Operating System: macOS"
    else
        print_error "Unsupported operating system: $OSTYPE"
        print_info "SIRAJ requires Linux or macOS for optimal performance"
        exit 1
    fi
    
    # Check memory
    if command -v free &> /dev/null; then
        MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
        if [[ $MEMORY_GB -lt 8 ]]; then
            print_error "Insufficient memory: ${MEMORY_GB}GB available, 8GB required"
            print_info "Please upgrade your system memory for optimal AI performance"
            exit 1
        else
            print_success "Memory: ${MEMORY_GB}GB available"
        fi
    elif [[ "$OS" == "macos" ]]; then
        MEMORY_GB=$(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 ))
        if [[ $MEMORY_GB -lt 8 ]]; then
            print_error "Insufficient memory: ${MEMORY_GB}GB available, 8GB required"
            exit 1
        else
            print_success "Memory: ${MEMORY_GB}GB available"
        fi
    fi
    
    # Check disk space
    DISK_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [[ $DISK_SPACE -lt 20 ]]; then
        print_error "Insufficient disk space: ${DISK_SPACE}GB available, 20GB required"
        print_info "Please free up disk space for AI models and system components"
        exit 1
    else
        print_success "Disk space: ${DISK_SPACE}GB available"
    fi
    
    # Check for GPU (optional but recommended)
    if command -v nvidia-smi &> /dev/null; then
        GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2>/dev/null | head -1)
        if [ $? -eq 0 ]; then
            print_success "GPU detected: $GPU_INFO (will enable GPU acceleration)"
            export ENABLE_GPU=true
        fi
    else
        print_info "No GPU detected, using CPU inference (slower but functional)"
        export ENABLE_GPU=false
    fi
}

# Install Docker if not present
install_docker() {
    if ! command -v docker &> /dev/null; then
        print_status "Installing Docker..."
        
        if [[ "$OS" == "linux" ]]; then
            # Install Docker on Linux
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo usermod -aG docker $USER
            print_success "Docker installed. Please log out and back in, then re-run this script."
            exit 0
        elif [[ "$OS" == "macos" ]]; then
            print_error "Please install Docker Desktop for Mac from: https://docs.docker.com/docker-for-mac/install/"
            exit 1
        fi
    else
        print_success "Docker is installed"
    fi
    
    # Check if Docker is running
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose not found. Please install docker-compose."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are ready"
}

# Install Ollama
install_ollama() {
    if ! command -v ollama &> /dev/null; then
        print_status "Installing Ollama AI engine..."
        
        if [[ "$OS" == "linux" ]]; then
            curl -fsSL https://ollama.ai/install.sh | sh
        elif [[ "$OS" == "macos" ]]; then
            if command -v brew &> /dev/null; then
                brew install ollama
            else
                print_error "Please install Homebrew first, then run: brew install ollama"
                exit 1
            fi
        fi
        
        print_success "Ollama installed successfully"
    else
        print_success "Ollama is already installed"
    fi
    
    # Start Ollama service
    print_status "Starting Ollama service..."
    if [[ "$OS" == "linux" ]]; then
        # Start as background service
        ollama serve &
        OLLAMA_PID=$!
        sleep 5
    elif [[ "$OS" == "macos" ]]; then
        # Start as background service
        brew services start ollama
        sleep 5
    fi
    
    # Verify Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        print_success "Ollama service is running"
    else
        print_error "Failed to start Ollama service"
        exit 1
    fi
}

# Download and configure Gemma models
setup_gemma_models() {
    print_status "Setting up Gemma 3n educational models..."
    print_info "This may take 10-20 minutes depending on your internet connection"
    
    # Check if models are already downloaded
    if ollama list | grep -q "gemma2:9b"; then
        print_success "Gemma models already available"
        return
    fi
    
    printf "${CYAN}📚 Downloading primary educational model (Gemma 2 9B)...${NC}\n"
    if ollama pull gemma2:9b-instruct-q4_k_m; then
        print_success "Primary model downloaded"
    else
        print_error "Failed to download primary model"
        exit 1
    fi
    
    printf "${CYAN}📚 Downloading lightweight model (Gemma 2 2B)...${NC}\n"
    if ollama pull gemma2:2b-instruct-q4_k_m; then
        print_success "Lightweight model downloaded"
    else
        print_error "Failed to download lightweight model"
        exit 1
    fi
    
    # Configure educational personalities
    print_status "Configuring AI teaching personalities..."
    
    # Create custom educational models with different personalities
    cat > /tmp/socratic_teacher.modelfile << 'EOF'
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
EOF

    cat > /tmp/constructivist_teacher.modelfile << 'EOF'
FROM gemma2:9b-instruct-q4_k_m
SYSTEM """You are a Constructivist teacher, one of seven AI archetypes in the SIRAJ Educational Council.

Your role is to promote learning through construction, experimentation, and hands-on discovery. You believe students learn best by building understanding through direct experience.

Key principles:
- Suggest hands-on activities and experiments
- Encourage building, making, and creating
- Connect new knowledge to prior experience
- Promote trial-and-error learning
- Use real-world applications and examples

Provide concrete activities students can do to explore concepts. Always consider what materials or tools might be available in a typical learning environment."""

PARAMETER temperature 0.8
PARAMETER top_p 0.9
EOF

    # Create the custom models
    ollama create socratic_teacher -f /tmp/socratic_teacher.modelfile
    ollama create constructivist_teacher -f /tmp/constructivist_teacher.modelfile
    
    print_success "Educational AI personalities configured"
}

# Setup the application environment
setup_application() {
    print_status "Setting up SIRAJ Educational AI application..."
    
    # Create environment file
    cat > .env << EOF
# SIRAJ Educational AI Configuration
SIRAJ_VERSION=8.1.0
SIRAJ_MODE=educational
DEPLOYMENT_TYPE=development

# AI Configuration
OLLAMA_HOST=http://localhost:11434
GEMMA_PRIMARY_MODEL=gemma2:9b-instruct-q4_k_m
GEMMA_LIGHTWEIGHT_MODEL=gemma2:2b-instruct-q4_k_m
ENABLE_GPU=${ENABLE_GPU:-false}
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
SECRET_KEY=$(openssl rand -hex 32)
ACCESS_TOKEN_EXPIRE_MINUTES=1440
EOF

    print_success "Application environment configured"
}

# Build and start services
start_services() {
    print_status "Building and starting SIRAJ Educational services..."
    
    # Stop any existing containers
    docker-compose down
    
    # Pull latest base images
    print_status "Pulling Docker base images..."
    docker-compose pull
    
    # Build and start services
    print_status "Building custom educational AI containers..."
    docker-compose up --build -d
    
    if [ $? -ne 0 ]; then
        print_error "Failed to start services"
        exit 1
    fi
    
    print_success "Services started successfully"
    
    # Wait for services to be ready
    print_status "Waiting for services to initialize..."
    sleep 10
    
    # Health check
    MAX_ATTEMPTS=30
    ATTEMPT=1
    
    while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
        if curl -s http://localhost:8000/health > /dev/null; then
            print_success "Backend service is healthy"
            break
        fi
        
        printf "${YELLOW}⏳ Attempt $ATTEMPT/$MAX_ATTEMPTS - waiting for backend...${NC}\n"
        sleep 2
        ((ATTEMPT++))
    done
    
    if [ $ATTEMPT -gt $MAX_ATTEMPTS ]; then
        print_error "Backend service failed to start properly"
        print_info "Check logs with: docker-compose logs backend"
        exit 1
    fi
    
    # Check frontend
    if curl -s http://localhost:3000 > /dev/null; then
        print_success "Frontend service is healthy"
    else
        print_info "Frontend may still be initializing..."
    fi
}

# Display completion information
show_completion_info() {
    printf "\n${GREEN}"
    cat << "EOF"
🎓 SIRAJ Educational AI is now running!
===========================================
EOF
    printf "${NC}\n"
    
    printf "${CYAN}📊 Educational Dashboard: ${NC}http://localhost:3000\n"
    printf "${CYAN}📚 API Documentation: ${NC}http://localhost:8000/docs\n"
    printf "${CYAN}🔍 Health Check: ${NC}http://localhost:8000/health\n"
    printf "${CYAN}🧠 AI Council Status: ${NC}http://localhost:8000/council/status\n\n"
    
    printf "${BLUE}🎯 What you can do now:${NC}\n"
    printf "   • Open the dashboard and start a tutoring session\n"
    printf "   • Submit homework for multi-perspective feedback\n"
    printf "   • Explore curriculum-aligned learning paths\n"
    printf "   • Watch the AI council debate educational topics\n\n"
    
    printf "${YELLOW}📝 Useful commands:${NC}\n"
    printf "   • View live logs: ${CYAN}docker-compose logs -f${NC}\n"
    printf "   • Stop system: ${CYAN}docker-compose down${NC}\n"
    printf "   • Restart system: ${CYAN}docker-compose restart${NC}\n"
    printf "   • Update models: ${CYAN}ollama pull gemma2:9b-instruct-q4_k_m${NC}\n\n"
    
    printf "${PURPLE}🌟 Pro Tips:${NC}\n"
    printf "   • Try asking the same question to different AI teachers\n"
    printf "   • Upload homework assignments for detailed feedback\n"
    printf "   • Use the curriculum overlay to align with standards\n"
    printf "   • Check the analytics dashboard for learning insights\n\n"
}

# Main execution flow
main() {
    printf "${PURPLE}🚀 Initializing SIRAJ Educational AI...${NC}\n\n"
    
    check_system_requirements
    install_docker
    install_ollama
    setup_gemma_models
    setup_application
    start_services
    show_completion_info
    
    # Optional: show logs
    printf "${YELLOW}Would you like to view live application logs? (y/N): ${NC}"
    read -r SHOW_LOGS
    
    if [[ $SHOW_LOGS =~ ^[Yy]$ ]]; then
        printf "\n${CYAN}📊 Live Application Logs (Press Ctrl+C to exit):${NC}\n"
        docker-compose logs -f
    fi
}

# Handle cleanup on exit
cleanup() {
    printf "\n${YELLOW}🛑 Cleaning up...${NC}\n"
    if [[ -n $OLLAMA_PID ]]; then
        kill $OLLAMA_PID 2>/dev/null
    fi
}

# Set trap for cleanup
trap cleanup EXIT

# Run main function
main "$@"