# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install uv and copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --no-default-features

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Run the FastAPI application using uvicorn
# pk_internal_tools/pk_web_server/main.py 경로에 있는 app 객체를 실행
CMD ["uvicorn", "pk_internal_tools.pk_web_server.main:app", "--host", "0.0.0.0", "--port", "8000"]
