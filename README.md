# 🏠 Axonius Airbnb UI Automation

Automated UI testing framework for Airbnb using **Playwright**, **Pytest**, and **Docker**.
Includes a custom timeout plugin to forcefully stop the test suite after a specified duration.

---

## 1. Clone the Repository

```bash
git clone https://github.com/Ni172/airbnb-automation.git
cd airbnb-automation
```

---

## 2. Build the Docker Image

Use the base image `mcr.microsoft.com/playwright/python:v1.43.0-jammy` because it comes pre-installed with:

* Python 3.10 and pip
* Playwright CLI and core libraries
* Headless browser support (Chromium by default)
* Ubuntu Jammy (22.04) for stability and compatibility

This image eliminates the need to manually install browser dependencies, making it ideal for Playwright automation in CI/CD and Dockerized environments.

**Docker command:**

```bash
docker build -t airbnb-test -f docker/Dockerfile .
```

Or use:

```bash
make build
```
> ⚠️ **Note:** The `make build` (or `docker build`) process may take several minutes to complete, especially the first time, as it installs dependencies and browsers inside the container.

This builds a clean Docker environment with:

* Python dependencies
* Playwright browsers (Chromium by default)
* Your custom Pytest plugin

---

## 3. Running the Tests

### Run all tests:

```bash
docker run --rm -v $(pwd):/app -w /app airbnb-test pytest tests/ -v
```

Or use:

```bash
make test
```

---

### Run tests with a suite timeout (e.g., 30 seconds):

```bash
docker run --rm -v $(pwd):/app -w /app airbnb-test pytest tests/ --suite-timeout=30 -v
```

---

### Run tests with a different browser (default is Chromium):

```bash
docker run --rm -v $(pwd):/app -w /app airbnb-test pytest tests/ --browser=webkit -v
```

Supported values: `chromium`, `firefox`, `webkit`

---

## 4. Clean Docker Images & Volumes

```bash
make clean
```

This will remove unused containers, images, volumes, and cache.

---

## 5. Docker Command Summary

| Command                                                                                  | Description             |
| ---------------------------------------------------------------------------------------- | ----------------------- |
| `docker build -t airbnb-test -f docker/Dockerfile .`                                     | Build Docker image      |
| `docker run --rm -v $(pwd):/app -w /app airbnb-test pytest tests/ -v`                    | Run tests               |
| `docker run --rm -v $(pwd):/app -w /app airbnb-test pytest tests/ --suite-timeout=30 -v` | Run with timeout        |
| `docker run --rm -v $(pwd):/app -w /app airbnb-test pytest tests/ --browser=webkit -v`   | Run with WebKit browser |
| `docker system prune -af --volumes`                                                      | Clean Docker system     |

---

