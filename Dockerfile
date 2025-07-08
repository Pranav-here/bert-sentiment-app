# Use a slightly larger base to avoid C++/lib errors
FROM python:3.10

# Set working directory
WORKDIR /app

# System-level packages required for torch, pandas, pyarrow, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libssl-dev \
    libffi-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install CPU-compatible torch first
COPY requirements.txt .

# Install torch separately to avoid broken wheels
RUN pip install --no-cache-dir torch==2.0.1+cpu torchvision==0.15.2+cpu \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Then install the rest of the packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]