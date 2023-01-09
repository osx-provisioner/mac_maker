ARG PYTHON_VERSION=3.8
FROM python:$PYTHON_VERSION-slim AS base

LABEL maintainer="niall@niallbyrne.ca"
LABEL project="mac_maker"
LABEL environment=""

ENV PYTHONUNBUFFERED 1
ENV PROJECT_NAME "mac_maker"
ENV PIB_CONFIG_FILE_LOCATION "/app/assets/cli.yml"

ENV VERSION_GITLEAKS "v7.2.0"
ENV VERSION_POETRY "poetry<1.4.0"

# Mark Container
RUN echo "mac_maker" > /etc/container_release

# Install Base Dependencies
RUN apt-get update               && \
    apt-get upgrade -y           && \
    apt-get install -y              \
    --no-install-recommends         \
    bash=5.*                        \
    build-essential=12.*         && \
    rm -rf /var/lib/apt/lists/*

# Setup directories
RUN mkdir -p /home/user /app
WORKDIR /app

# Create the runtime user, and enforce permissions
RUN useradd user -d /home/user           \
                 -s /bin/bash            \
                 -M                   && \
 chown -R user:user /home/user        && \
 chown -R user:user /app

# Include the local binary folder in PATH
ENV PATH "/home/user/.local/bin/:${PATH}"

# ======================================================

# Poetry Intermediary
FROM base AS poetry

LABEL environment=""

# Install Poetry
RUN pip install --no-cache-dir "${VERSION_POETRY}"

# ======================================================

# Development Environment
FROM poetry AS development
LABEL environment="DEVELOPMENT"
ENV ENVIRONMENT DEVELOPMENT

# Install Dev Dependencies
RUN apt-get update                      && \
    apt-get install -y                     \
    --no-install-recommends                \
    curl=7.74.*                            \
    fish=3.1.*                             \
    golang-github-pelletier-go-toml=1.8.*  \
    jq=1.6*                                \
    openssh-client=1:8.*                   \
    shellcheck=0.7.*                       \
    sudo=1.9.*                             \
    tig=2.5.*                              \
    vim=2:8.*

# Install Git Leaks
RUN curl --fail -sL "https://github.com/zricethezav/gitleaks/releases/download/${VERSION_GITLEAKS}/gitleaks-linux-amd64"    \
    -o /usr/bin/gitleaks                                                                                                 && \
    chmod +x /usr/bin/gitleaks

# Add user to sudoers, and make the default user
RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set the runtime user
USER user

# Copy the poetry configuration
COPY pyproject.toml *.lock /app/

# Cache Dependencies
RUN poetry install --no-root -E docs

# Copy the Codebase
COPY . /app

# Install the Application
RUN poetry install -E docs

# Create A Symlink For the Bash Customizations
RUN ln -sf /app/assets/.bash_customize /home/user/.bash_customize

# Setup The Dev CLI
RUN poetry run dev setup-bash

CMD ["./mac_maker/container_init.sh"]

# ======================================================

# Pre Production Environment
FROM poetry as pre_production

LABEL environment="PRE_PRODUCTION"

ENV ENVIRONMENT "PRE_PRODUCTION"

# Set the runtime user
USER user

# Copy the poetry configuration
COPY pyproject.toml *.lock /app/

# Export the lock file
RUN poetry lock
RUN poetry export --without-hashes -f requirements.txt -o /app/requirements.txt

# Copy the codebase
COPY . /app

# ======================================================

# Production Environment
FROM base as production

LABEL environment="PRODUCTION"

ENV ENVIRONMENT "PRODUCTION"

# Set the runtime user
USER user

# Copy the requirements.txt file from pre_production
COPY --from=pre_production /app/requirements.txt /app/requirements.txt

# Install Production Packages Only
RUN pip --no-cache-dir install -r requirements.txt

# Copy the codebase
COPY . /app

CMD ["./mac_maker/container_init.sh"]
