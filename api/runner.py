import os
import tempfile
import subprocess
import shutil
import json

def run_code(code: str):
    # Create temp dir for isolation of the script file
    tmpdir = tempfile.mkdtemp(prefix="sce_")
    script_path = os.path.join(tmpdir, "script.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)

    # Build docker run command
    # Start simple (security added later); use timeout via 'timeout' utility from h]
    cmd = [
    "docker", "run", "--rm",
    "--network", "none",          # block outbound/inbound network
    "--memory", "128m",           # cap memory
    "--memory-swap", "128m",      # no swap expansion
    "--pids-limit", "64",         # prevent fork bombs
    "--cpus", "0.5",              # keep CPU usage modest
    "-v", f"{script_path}:/app/script.py:ro",
    "safe-python:latest"
]

    try:
        # Use a host-side timeout to avoid hung containers (10s)
        result = subprocess.run(
            ["timeout", "--signal=SIGKILL", "10s"] + cmd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode == 124:
            # 124 is timeout’s exit code on timeout
            return {"error": "Execution timed out after 10 seconds"}
        elif result.returncode != 0:
            # Return stderr in a safe, minimal way
            return {"error": result.stderr.strip()[:2000] or "Execution failed"}
        else:
            return {"output": result.stdout}
    except FileNotFoundError as e:
        # If 'timeout' is not available on the host (Windows PowerShell), fallback to Python timeout
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            if result.returncode != 0:
                return {"error": result.stderr.strip()[:2000] or "Execution failed"}
            return {"output": result.stdout}
        except subprocess.TimeoutExpired:
            return {"error": "Execution timed out after 10 seconds"}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
