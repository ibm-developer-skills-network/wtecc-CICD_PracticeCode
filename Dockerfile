FROM python:3.9-slim

# Establish a working folder
WORKDIR /app

# Establish dependencies
COPY requirements.txt .
RUN python -m pip install -U pip wheel && \
    pip install -r requirements.txt

# Copy source files last because they change the most
COPY service ./service

# Become non-root user
RUN useradd -m -r service && \
    chown -R service:service /app
USER service

# Run the service on port 8080
EXPOSE 8080
CMD ["gunicorn", "service:app", "--bind", "0.0.0.0:8080"]
