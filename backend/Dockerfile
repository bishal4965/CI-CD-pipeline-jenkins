FROM python:3.9-slim

# Create non-root user
RUN useradd -m appuser

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Start application
CMD ["gunicorn", "--timeout", "120", "--workers", "2", "-b", "0.0.0.0:5000", "app:app"]
