# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory to the container
COPY . .

# Expose the port that your FastAPI application listens on (change it to your app's port if necessary)
EXPOSE 8000

# Start the FastAPI application when the container is run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

