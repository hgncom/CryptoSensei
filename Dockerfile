# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files into the container
COPY server.py .
COPY openapi.yaml .
COPY ai-plugin.json .

# Install the required dependencies
RUN pip install fastapi requests uvicorn cachetools

# Expose the port that your FastAPI server is listening on (e.g., 8000)
EXPOSE 8080

# Command to run your FastAPI server when the container starts
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
