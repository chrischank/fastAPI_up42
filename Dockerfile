FROM continuumio/miniconda3:latest

RUN apt update && apt upgrade

# Set the current working directory to /code.
#This is where we'll put the environment.yml file and the fastAPI directory.
WORKDIR /code

# Copy the file with the requirements to the /code directory.
COPY ./env_explicit.yml /code/environment.yml

RUN conda config --set restore_free_channel true
RUN conda env create -f environment.yml

# Activate env
ENV PATH /opt/conda/envs/api_up42/bin:$PATH
RUN /bin/bash -c "source activate api_up42"

EXPOSE 80

# Copy fastAPI to docker main folder
COPY ./fastAPI /code/app

# Testing folder
#COPY ./test /code/app

WORKDIR /code/app

# Set the command to run the uvicorn server.
CMD python -m uvicorn main:app --host 0.0.0.0 --port 80

# Set the command to run the test using pytest.
#CMD python -m pytest