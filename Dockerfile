# Use a base image (e.g., Ubuntu)
FROM ubuntu:20.04

# Set environment variable to avoid tzdata prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages, including libgpg-error and virtualenv
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    autoconf \
    automake \
    libtool \
    pkg-config \
    python3 \
    python3-pip \
    wget \
    git \
    libgpg-error-dev \
    gpg-agent \
    tzdata \
    python3-venv \
    pinentry-tty \
    && apt-get clean

# Clone and install Libgcrypt 1.8.4
RUN git clone --branch LIBGCRYPT-1.8-BRANCH https://github.com/gpg/libgcrypt.git && \
    cd libgcrypt && \
    ./autogen.sh && \
    ./configure --disable-doc && \
    make && \
    make install && \
    ldconfig

# Clean up
RUN rm -rf libgcrypt

# Configure GPG for non-interactive mode
RUN mkdir -p /root/.gnupg && \
    echo "use-agent" >> /root/.gnupg/gpg.conf && \
    echo "pinentry-program /usr/bin/pinentry-tty" >> /root/.gnupg/gpg-agent.conf && \
    chmod 700 /root/.gnupg

# Set the working directory
WORKDIR /app

# Copy your Python code to the container
COPY . .

COPY libgcrypt_wrapper.py .


# Create a virtual environment and install Python dependencies
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to use the virtual environment
CMD ["/bin/bash", "-c", "source venv/bin/activate && python3 repeated_signings.py"]
