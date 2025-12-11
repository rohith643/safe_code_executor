# Minimal, fast, deterministic runtime
FROM python:3.11-slim

# Create unprivileged user (advanced hardening later)
RUN useradd -m runner

# Workdir
WORKDIR /app

# No extra deps: we'll only run user script
COPY entrypoint.sh /app/entrypoint.sh

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Switch to non-root for better safety (you can add this later in Advanced)
USER runner

# Default command expects script.py to be present in the container
ENTRYPOINT ["/app/entrypoint.sh"]
