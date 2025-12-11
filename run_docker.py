#!/usr/bin/env python3
"""
Simple Docker runner for AI Semantic Search project
"""

import subprocess
import os
import sys


def print_section(title):
    """Print a section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def run_command(cmd, description):
    """Run a shell command and print output"""
    print(f"\n📋 {description}")
    print(f"   Command: {' '.join(cmd)}")
    print("-" * 40)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"⚠️  Errors:\n{result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print_section("AI SEMANTIC SEARCH - DOCKER RUNNER")
    print("Student: YN3012170034")
    print("Project: Docker Containerization with ML/NLP")

    # Check Docker installation
    print_section("1. VERIFY DOCKER INSTALLATION")
    docker_ok = run_command(["docker", "--version"], "Check Docker version")

    if not docker_ok:
        print("\n❌ Docker is not installed or not in PATH")
        print("Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/")
        sys.exit(1)

    # List Docker images
    print_section("2. CHECK EXISTING DOCKER IMAGES")
    run_command(["docker", "images"], "List Docker images")

    # Build Docker image
    print_section("3. BUILD DOCKER IMAGE")
    print("Building 'ai-semantic-search' image from current directory...")

    build_ok = run_command(
        ["docker", "build", "-t", "ai-semantic-search", "."],
        "Build Docker image"
    )

    if not build_ok:
        print("\n❌ Docker build failed!")
        print("Trying alternative approach...")

        # Try creating a simple Dockerfile if it doesn't exist
        if not os.path.exists("Dockerfile"):
            print("Creating simple Dockerfile...")
            with open("Dockerfile", "w") as f:
                f.write("""FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install streamlit
CMD ["streamlit", "run", "--server.port=8501", "--server.address=0.0.0.0"]
""")
            build_ok = run_command(
                ["docker", "build", "-t", "ai-semantic-search", "."],
                "Build with simple Dockerfile"
            )

    # Run container if build was successful
    if build_ok:
        print_section("4. RUN DOCKER CONTAINER")
        print("Starting AI Semantic Search application on port 8501...")
        print("Press Ctrl+C to stop the container")
        print("\n🌐 Open browser to: http://localhost:8501")
        print("-" * 40)

        try:
            # Run the container
            run_command([
                "docker", "run", "-p", "8501:8501",
                "--name", "ai-search-app",
                "ai-semantic-search"
            ], "Run Docker container")
        except KeyboardInterrupt:
            print("\n\n🛑 Container stopped by user")

    # Cleanup option
    print_section("5. CLEANUP COMMANDS")
    print("To clean up Docker resources:")
    print("  docker stop ai-search-app")
    print("  docker rm ai-search-app")
    print("  docker rmi ai-semantic-search")
    print("\n✅ Docker runner completed!")


if __name__ == "__main__":
    main()