# Use the official Python image with Playwright support
FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

# Set working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Install only necessary Playwright browsers (use full install if needed)
RUN playwright install

# Set default command to run tests
CMD ["pytest", "tests/", "-s"]
