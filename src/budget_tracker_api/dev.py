"""Development server script that builds frontend and runs FastAPI."""
import subprocess
import sys
import signal
import time
from pathlib import Path


def check_command(command: str) -> bool:
    """Check if a command is available in PATH."""
    try:
        subprocess.run(
            ["which", command],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def ensure_npm_deps(frontend_dir: Path) -> None:
    """Install npm dependencies if node_modules doesn't exist."""
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        print("✅ Dependencies installed!")
        print()


def initial_build(frontend_dir: Path) -> None:
    """Run initial frontend build."""
    print("📦 Building frontend (initial build)...")
    subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
    print()
    print("✅ Initial build complete!")
    print()


def start() -> None:
    """Start development servers for frontend and backend."""
    # Get paths
    script_dir = Path(__file__).resolve().parent
    frontend_dir = script_dir / "frontend"

    # Check prerequisites
    if not check_command("npm"):
        print("❌ Error: npm is not installed")
        sys.exit(1)

    if not frontend_dir.exists():
        print(f"❌ Error: Frontend directory not found at {frontend_dir}")
        sys.exit(1)

    print("🚀 Starting Budget Tracker Development Server")
    print()

    # Ensure npm dependencies are installed
    ensure_npm_deps(frontend_dir)

    # Initial build
    initial_build(frontend_dir)

    print("🔄 Starting watch mode + FastAPI server...")
    print()
    print("   Frontend: Auto-rebuilding on file changes")
    print("   Backend:  http://localhost:8000")
    print()
    print("Press Ctrl+C to stop both servers")
    print()

    # Start frontend build in watch mode
    watch_process = subprocess.Popen(
        ["npm", "run", "build:watch"],
        cwd=frontend_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Give watch mode a moment to start
    time.sleep(2)

    # Start FastAPI server
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn",
         "budget_tracker_api.app.main:app",
         "--host", "0.0.0.0",
         "--port", "8000",
         "--reload"]
    )

    def cleanup(signum, frame):
        """Cleanup handler for graceful shutdown."""
        print()
        print("🛑 Stopping servers...")
        watch_process.terminate()
        api_process.terminate()

        # Wait for processes to terminate
        try:
            watch_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            watch_process.kill()

        try:
            api_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_process.kill()

        sys.exit(0)

    # Set up signal handlers
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # Wait for API process (main process)
    try:
        api_process.wait()
    except KeyboardInterrupt:
        cleanup(None, None)


if __name__ == "__main__":
    start()
