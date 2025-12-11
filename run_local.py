
import subprocess
import sys
import os
import time


def install_pytorch():
    """Install PyTorch specifically"""
    print("🔧 Installing PyTorch (this may take a few minutes)...")

    # Try different installation methods
    methods = [
        # CPU-only version (fastest)
        [sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "--index-url",
         "https://download.pytorch.org/whl/cpu"],

        # Standard pip
        [sys.executable, "-m", "pip", "install", "torch"],

        # With specific version
        [sys.executable, "-m", "pip", "install", "torch==2.0.1"]
    ]

    for method in methods:
        try:
            subprocess.check_call(method)
            print("✅ PyTorch installed successfully")
            return True
        except subprocess.CalledProcessError:
            continue

    print("❌ Failed to install PyTorch with all methods")
    return False


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'streamlit': 'streamlit',
        'sentence_transformers': 'sentence-transformers',
        'chromadb': 'chromadb',
        'torch': 'torch',
        'pandas': 'pandas',
        'plotly': 'plotly',
        'sklearn': 'scikit-learn',
        'numpy': 'numpy'
    }

    print("🔍 Checking dependencies...")
    missing_packages = []

    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} not found")
            missing_packages.append(package_name)

    return missing_packages


def install_dependencies(missing_packages):
    """Install missing packages"""
    print(f"📦 Installing {len(missing_packages)} missing packages...")

    # Install PyTorch separately if needed
    if 'torch' in missing_packages:
        if not install_pytorch():
            return False
        missing_packages.remove('torch')

    # Install remaining packages
    if missing_packages:
        try:
            subprocess.check_call([
                                      sys.executable, "-m", "pip", "install"
                                  ] + missing_packages)
            print("✅ All packages installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            return False

    return True


def run_application():
    """Run the Streamlit application"""
    print("\n" + "=" * 60)
    print("🚀 STARTING AI SEMANTIC SEARCH ENGINE")
    print("=" * 60)
    print("\n📊 Open your browser and go to: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("⏳ Starting server...\n")

    time.sleep(2)  # Give user time to read

    try:
        # Run streamlit
        subprocess.call([
            sys.executable, "-m", "streamlit",
            "run", "app/main.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--theme.base=light",
            "--server.fileWatcherType=none",
            "--browser.serverAddress=localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")


def create_simple_app():
    """Create a simpler version if dependencies fail"""
    print("\n⚠️  Creating simplified version...")

    simple_code = '''
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="AI Search", page_icon="🔍", layout="wide")

st.title("🤖 AI Semantic Search Engine")
st.markdown("---")

# Simple search without ML
st.header("🔍 Simple Text Search")
query = st.text_input("Enter search query:")

sample_data = [
    "Machine learning is a subset of artificial intelligence.",
    "Deep learning uses neural networks with multiple layers.",
    "Natural Language Processing enables computers to understand human language.",
    "Transformers have revolutionized NLP with attention mechanisms.",
    "BERT is a transformer model for language understanding."
]

if query:
    query_lower = query.lower()
    results = []

    for text in sample_data:
        if query_lower in text.lower():
            results.append(text)

    if results:
        st.success(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            st.markdown(f"**Result {i}:** {result}")
    else:
        st.warning("No results found.")

# System info
st.markdown("---")
st.header("⚙️ System Information")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Documents", len(sample_data))
with col2:
    st.metric("Search Method", "Keyword")
with col3:
    st.metric("Status", "Online")

st.info("Note: Full semantic search requires PyTorch installation.")
'''

    with open("app/simple_main.py", "w") as f:
        f.write(simple_code)

    return "app/simple_main.py"


def main():
    """Main function"""
    print("=" * 60)
    print("🤖 AI SEMANTIC SEARCH ENGINE - LOCAL RUNNER")
    print("=" * 60)

    # Check directory
    if not os.path.exists("app"):
        print("❌ Error: 'app' directory not found")
        print("💡 Please run this script from the project root directory")
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Check dependencies
    missing = check_dependencies()

    if missing:
        print(f"\n⚠️  Found {len(missing)} missing dependencies")
        response = input("Do you want to install them? (y/n): ").lower().strip()

        if response == 'y':
            if not install_dependencies(missing):
                print("\n⚠️  Some dependencies failed to install.")
                response = input("Run simplified version instead? (y/n): ").lower().strip()
                if response == 'y':
                    app_file = create_simple_app()
                    subprocess.call([
                        sys.executable, "-m", "streamlit",
                        "run", app_file,
                        "--server.port=8501"
                    ])
                sys.exit(1)
        else:
            print("❌ Cannot run without required dependencies")
            sys.exit(1)

    # Run the application
    run_application()


if __name__ == "__main__":
    main()