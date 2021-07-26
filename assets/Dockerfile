ARG PYTHON_VERSION=3.8
FROM python:$PYTHON_VERSION-slim AS base
MAINTAINER niall@niallbyrne.ca
ENV PYTHONUNBUFFERED 1
ENV PROJECT_NAME "mac_maker"
ENV PIB_CONFIG_FILE_LOCATION "/app/assets/cli.yml"
ENV POETRY_VIRTUALENVS_CREATE "false"
LABEL PROJECT=mac_maker

# Mark Container
RUN echo "mac_maker" > /etc/container_release

# Install Base Dependencies
RUN apt-get update      && \
    apt-get upgrade -y  && \
    apt-get install -y     \
    bash                   \
    build-essential

# Setup directories
RUN mkdir -p /home/user /app
WORKDIR /app

# Create the runtime user, and enforce permissions
RUN useradd user -d /home/user        \
                 -s /bin/bash         \
                 -M                   \
 && chown -R user:user /home/user     \
 && chown -R user:user /app

# Install Latest Poetry
RUN pip install poetry             && \
    pip install --upgrade pip      && \
    mkdir -p /usr/local/src        && \
    chown user:user /usr/local/src

# Include the local binary folder in PATH
ENV PATH "/home/user/.local/bin/:${PATH}"

# ======================================================

# Development Environment
FROM base AS development
LABEL ENVIRONMENT=DEVELOPMENT
ENV ENVIRONMENT=DEVELOPMENT
ENV GITLEAKSVERSION="v7.2.0"

# Install Dev Dependencies
RUN apt-get install -y              \
    curl                            \
    fish                            \
    golang-github-pelletier-go-toml \
    jq                              \
    openssh-client                  \
    shellcheck                      \
    sudo                            \
    tig                             \
    vim

# Install Git Leaks
RUN curl --fail -sL "https://github.com/zricethezav/gitleaks/releases/download/${GITLEAKSVERSION}/gitleaks-linux-amd64"    \
    -o /usr/bin/gitleaks                                                                                                && \
    chmod +x /usr/bin/gitleaks

# Add user to sudoers, and make the default user
RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set the runtime user
USER user

# Copy the codebase
COPY . /app

# Create A Symlink For the Bash Customizations
RUN ln -sf /app/assets/.bash_customize /home/user/.bash_customize

# https://github.com/python-poetry/poetry/issues/3321
RUN mkdir -p /home/user/.local/lib/python${PYTHON_VERSION}/site-packages && \
    mkdir -p /home/user/.local/bin

# Setup The Dev CLI
RUN poetry lock                                                 && \
    poetry install                                              && \
    dev setup-bash

CMD ["./mac_maker/container_init.sh"]

# ======================================================

# Production Environment
FROM base as production
LABEL ENVIRONMENT=PRODUCTION
ENV ENVIRONMENT=PRODUCTION

# Copy the codebase
USER user
COPY . /app

# Install the Production Dependencies
USER root

# https://github.com/python-poetry/poetry/issues/3321
RUN mkdir -p /home/user/.local/lib/python${PYTHON_VERSION}/site-packages && \
    mkdir -p /home/user/.local/bin

RUN poetry lock                                                 && \
    poetry install --no-dev                                     && \
    pip uninstall -y poetry

# Set the Runtime User
USER user

CMD ["./mac_maker/container_init.sh"]
