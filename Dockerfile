FROM python:3.9-slim

# Install system dependencies if your project needs them (uncomment if needed)
# RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install Python dependencies
COPY MMU-VR-Study-Group/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy Django project code
COPY MMU-VR-Study-Group/ .

# Expose port for Daphne
EXPOSE 8000

# Run Daphne ASGI server (collectstatic should be run in a startup script or CI/CD step)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "storefront.asgi:application"]