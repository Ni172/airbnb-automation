# Use the official Python image with Playwright support
FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

# Set working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project (including your plugin)
COPY . .

# Install your custom Pytest plugin from local setup.py
RUN pip install .

# Install Playwright browsers
RUN playwright install --with-deps

# Set default command to run tests
CMD ["pytest", "tests/", "-s"]
