# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY recipe_service ./recipe_service

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic pydantic-settings

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()"

# Run the server
CMD ["uvicorn", "recipe_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
