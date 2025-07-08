# Start from an official Python image (you don’t install Python yourself)
FROM python:3.10-slim

# Set the folder *inside the container* where your code will live
WORKDIR /app

# Copy your list of Python dependencies into the container
COPY requirements.txt .

# Install dependencies *inside* the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other project files into the container (your code)
COPY . .

# Tell Docker that our app will listen on port 8000
EXPOSE 8000

# When the container starts, run this command to launch the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
