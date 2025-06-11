FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory in the container
WORKDIR /app

# Copy only requirements first for caching
COPY MMU-VR-Study-Group/requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt


# Copy the Django project code into the container
COPY MMU-VR-Study-Group/ /app/

RUN python manage.py collectstatic --noinput

# Expose port 8000 for Daphne
EXPOSE 8000

# Run Daphne ASGI server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "storefront.asgi:application"]
