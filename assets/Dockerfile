ARG BUILD_ARG_PYTHON_VERSION=3.11

FROM python:$BUILD_ARG_PYTHON_VERSION-slim AS base

ARG BUILD_ARG_CONTAINER_GID=1000
ARG BUILD_ARG_CONTAINER_UID=1000

LABEL maintainer="niall@niallbyrne.ca"
LABEL project="mac_maker"
LABEL environment=""

ENV PYTHONUNBUFFERED 1
ENV PROJECT_NAME "mac_maker"
ENV PIB_CONFIG_FILE_LOCATION "/app/assets/cli.yml"

ENV VERSION_GITLEAKS "v7.2.0"
ENV VERSION_POETRY "poetry>=1.8.0,<1.9.0"
ENV VERSION_TOMLL "v1.9.4"

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

# Create the runtime user, and enforce permissions
RUN groupadd user -g "${BUILD_ARG_CONTAINER_GID}"
RUN useradd user -d /home/user                    \
                 -s /bin/bash                     \
                 -u "${BUILD_ARG_CONTAINER_UID}"  \
                 -g "${BUILD_ARG_CONTAINER_GID}"  \
                 -m

# Setup directories
RUN mkdir -p /app
RUN chown -R user:user /app
WORKDIR /app

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
    curl=7.88.*                            \
    fish=3.6.*                             \
    jq=1.6*                                \
    enchant-2=2.*                          \
    openssh-client=1:9.*                   \
    shellcheck=0.9.*                       \
    sudo=1.9.*                             \
    tig=2.5.*                              \
    vim=2:9.*

# Install tomll
RUN curl --fail -sL "https://github.com/pelletier/go-toml/releases/download/${VERSION_TOMLL}/tomll_linux_amd64.tar.xz"      \
    -o tomll.tar.xz                                                                                                      && \
    tar xvf tomll.tar.xz                                                                                                 && \
    mv tomll /usr/bin                                                                                                    && \
    chmod +x /usr/bin/tomll

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

# Enforce git repository permissions
USER root
RUN chown -R user:user /app
USER user

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

# Enforce git repository permissions
USER root
RUN chown -R user:user /app
USER user

CMD ["./mac_maker/container_init.sh"]
