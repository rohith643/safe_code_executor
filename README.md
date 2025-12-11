
**Project purpose**

A learning project to safely execute untrusted Python code inside Docker containers, with resource and network isolation.
Setup

- Build image: docker build -t safe-python:latest ./api/docker
- Install API deps: pip install flask flask-cors
- Run API: python api/app.py
- Open UI: web/index.html in browser (or serve via static server)

**API**

- Endpoint: POST /run
- Body: {"code":"print(2 + 2)"}
- Responses:
- Success: {"output":"4\n"}
- Error: {"error":"Execution timed out after 10 seconds"} or normalized error message
- Limits: Code length ≤ 5000 chars.
Security measures implemented
- Timeout: Host-side 10s timeout for container execution.
- Memory limit: --memory 128m, --memory-swap 128m.
- Network isolation: --network none.
- Process limit: --pids-limit 64.
- CPU limit: --cpus 0.5.
- Read-only FS: --read-only (optional, recommended).
- Non-root user: Container runs as runner (optional advanced; recommended).

**What I learned**

- What worked: Docker isolates filesystem and network; resource limits prevent abuse; timeouts reliably stop runaway code.
- What failed: Without limits, loops and memory bombs can hang or crash; write access exists unless explicitly read-only; network calls succeed unless disabled.
- Key insight: Docker is strong isolation but not a silver bullet. Safe execution requires layered controls: strict resource limits, no network, non-root, minimal images, no sensitive mounts, and clear timeouts.

**Demo steps**

- Normal code: Show print("Hello World").
- Security: Run infinite loop and see timeout; run memory hog and see memory error; attempt network call and see blocked.
- UI: Use the HTML page to submit code and view results/errors.

**Helpful implementation notes**

- Windows timeout: If GNU timeout isn’t available, rely on Python’s subprocess.run(..., timeout=10) as shown.
- Permissions: If you see “permission denied,” ensure you can run Docker without sudo (Linux: add user to docker group).
- Container not stopping: Verify timeout logic; add --pids-limit to prevent fork bombs.
- Slow runs: Use --cpus to cap CPU and keep host responsive.

**Bonus ideas**

- Node.js support: Build safe-node image with node:20-alpine, similar entrypoint.
- Syntax highlighting: Add CodeMirror or Monaco in the UI.
- Parallel runs: Queue requests and run up to 5 containers concurrently with a simple worker pool.
- Non-root + seccomp: Add --security-opt seccomp=... and --cap-drop ALL.
- Learn “container escape”: Research common misconfigurations (privileged mode,host mounts, vulnerable runtimes) and ways to reduce risk.

**Final deliverables checklist**

- Code:
- API: Clean Flask app with Docker integration and comments.
- Runner: Clear resource flags, timeout, sanitized errors.
- Docker image: Minimal Python, non-root user, simple entrypoint.
- Web UI: Simple HTML page to send code and display output.
- Git repository:
- Commits: Logical, small, with clear messages.
- Documentation:
- README: Setup, API examples, security features, short learning report.
- Tests: Scripts verifying functional and safety behavior.
