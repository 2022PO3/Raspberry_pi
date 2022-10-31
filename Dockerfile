FROM  python:3.10.7-slim-bullseye 

WORKDIR /packages
ENV PYTHONUNBUFFERED=1

# Copying the run script and making it executable.
COPY ./docker/run.sh ./docker/run.sh
RUN chmod +x ./docker/run.sh

# Copying all the package flies.
COPY ./anpr ./anpr

# Update pip
RUN python -m pip install --upgrade pip

# Install the different packages.
RUN pip3 install -r ./anpr/requirements.txt

ENTRYPOINT ["./docker/run.sh"]
