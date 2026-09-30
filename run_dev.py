"""Convenience launcher for local development.

Starts the FastAPI backend in a child process, waits until it is healthy,
launches the desktop client, then terminates the backend on exit.
"""

import subprocess
import sys
import time

import httpx


def wait_for_api(url: str, timeout: float = 12.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if httpx.get(url, timeout=0.5).status_code == 200:
                return
        except httpx.HTTPError:
            time.sleep(0.25)
    raise RuntimeError("TaskFlow API did not start in time")


def main() -> None:
    backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "task_manager.backend.main:app", "--host", "127.0.0.1", "--port", "8000"])
    try:
        wait_for_api("http://127.0.0.1:8000/health")
        subprocess.run([sys.executable, "-m", "task_manager"], check=False)
    finally:
        backend.terminate()
        try:
            backend.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend.kill()


if __name__ == "__main__":
    main()
