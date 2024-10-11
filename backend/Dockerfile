# Use an official Python 3.10 base image with a slim size
FROM python:3.10-slim

# Set the working directory
WORKDIR /backend

# Copy files from local to container
COPY . /backend/

# Install pip and setup environments
RUN echo "Setup environments"
RUN pip install --upgrade pip

# Install libraries and dependencies
RUN echo "Setup libraries and dependencies ..."
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install -r requirements.txt --no-cache-dir
RUN echo "Done setting up ${PWD}"