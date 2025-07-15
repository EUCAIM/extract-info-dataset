ARG BASE_IMG=python:3.13-slim

FROM $BASE_IMG

LABEL name="extract-info-dataset"
LABEL version="0.1"
LABEL image.source="https://github.com/EUCAIM/extract-info-dataset"
LABEL image.revision="ee9a1f92164d56c8a489025b8b4ccf8293106d5e"
LABEL image.version="0.1"

# Set defaults for build arguments
ARG USER_UID=1000
ARG USER_GID=1000

# Create non-root user and group, and prevent login
RUN groupadd -g $USER_GID eucaim && \
    useradd -u $USER_UID -g eucaim --create-home --shell /usr/sbin/nologin eucaim

COPY extract_info_dataset.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

# Set executable permissions (owned by root and read only by others)
RUN chown -R root:root /app && chmod 755 /app/extract_info_dataset.py

####### Switch to non-root user  ############
USER eucaim

ENTRYPOINT ["python3", "/app/extract_info_dataset.py"]
