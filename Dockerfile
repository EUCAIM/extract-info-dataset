FROM harbor.chaimeleon-eu.i3m.upv.es/chaimeleon-library-batch/ubuntu-python:latest

LABEL name="extract_info_dataset"
LABEL version="0.1"

COPY extract_info_dataset.py /opt/extract_info_dataset/
COPY requirements.txt /opt/extract_info_dataset/

RUN pip install --no-cache-dir -r /opt/extract_info_dataset/requirements.txt

ENTRYPOINT ["python3", "/opt/extract_info_dataset/extract_info_dataset.py"]