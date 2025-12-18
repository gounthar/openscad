# Multi-architecture Docker build for OpenSCAD
# Build command (from repository root):
# docker buildx build --platform linux/amd64,linux/arm64,linux/riscv64 -t gounthar/openscad:latest -f docker/Dockerfile .

# Use Debian Trixie as the base image
FROM debian:trixie-20251117-slim

# Install necessary packages and libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    coreutils \
    curl \
    git \
    gnupg \
    imagemagick \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    rsync \
    unzip \
    xauth \
    xvfb \
    cmake \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && python3 -m venv /tmp/venv \
    && /tmp/venv/bin/pip install --no-cache-dir \
        codespell \
        colorama \
        markdown \
        pillow \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Clone the upstream OpenSCAD repository
# Using specific commit for reproducible builds
ARG OPENSCAD_COMMIT=6ed120f28fcc410f593e9105080d190249c13753
RUN git clone https://github.com/openscad/openscad.git /openscad \
    && cd /openscad \
    && git checkout ${OPENSCAD_COMMIT} \
    && git submodule update --init --recursive

# Install dependencies and build OpenSCAD
RUN cd /openscad \
    && ./scripts/uni-get-dependencies.sh \
    && ./scripts/check-dependencies.sh \
    && cmake -B build -DEXPERIMENTAL=1 -DENABLE_TESTS=OFF \
    && cmake --build build -j$(nproc) \
    && cmake --install build --prefix /usr/local \
    && mkdir -p /output \
    && cp /usr/local/bin/openscad /output/

# Define the entrypoint
ENTRYPOINT ["/usr/local/bin/openscad"]
