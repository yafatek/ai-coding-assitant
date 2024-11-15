# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the WebSocket port (11203)
EXPOSE 11203

# Run the application with Uvicorn for WebSocket support
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "11203"]
