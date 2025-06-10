# Slim python version
FROM python:3.12.11-slim-bookworm

#Defined workdir
WORKDIR /app

#Copy only th requirements
COPY requirements /app/requirements

# Install python deps
RUN pip install --no-cache-dir -r /app/requirements/dev.txt

# Copy the project
COPY . /app/
