FROM mambaorg/micromamba:1.2.0

# Set the current working directory to /code.
#This is where we'll put the environment.yml file and the fastAPI directory.
WORKDIR /code

# Copy the file with the requirements to the /code directory.
# Copy the file with the requirements to the /code directory.
COPY ./environment.yml /code/environment.yml

RUN micromamba create --name api_up42 --yes --file /code/environment.yml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Activate env
ENV PATH /opt/conda/envs/api_up42/bin:$PATH

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
