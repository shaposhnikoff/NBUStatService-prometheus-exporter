FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN useradd -m -u 1000 exporter

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY currency.py .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Switch to non-root user
USER exporter

# Expose metrics port
EXPOSE 8000

# Run the application
CMD ["python", "currency.py"]
