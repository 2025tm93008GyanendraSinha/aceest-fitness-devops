# Use an official, lightweight Python base image for size optimization
FROM python:3.9-slim

# Create a non-root user for security compliance
RUN useradd -m aceestuser

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies without saving cache to keep the image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Transfer ownership of the app directory to the non-root user
RUN chown -R aceestuser:aceestuser /app

# Switch to the non-root user
USER aceestuser

# Expose the port the Flask app runs on
EXPOSE 5000

# Command to execute the application
CMD ["python", "app.py"]
