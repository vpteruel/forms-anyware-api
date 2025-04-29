FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including apt-utils
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    build-essential \
    curl \
    man-db \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN addgroup --system app && adduser --system --group app
USER app

# Use a virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies as non-root user
COPY --chown=app:app requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]