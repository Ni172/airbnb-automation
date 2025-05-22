# Use the official Python image with Playwright support
FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Install Playwright dependencies & browsers
RUN playwright install --with-deps

# Default command (override with `make run`)
CMD ["pytest", "tests/"]
