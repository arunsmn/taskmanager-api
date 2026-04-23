# Use official lightweight Python image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Install uv inside the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files FIRST (for Docker layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies only (no dev tools)
RUN uv sync --frozen --no-dev

# Copy the app code
COPY app/ ./app/

# Expose the port FastAPI runs on
EXPOSE 8000

# Start the server
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]