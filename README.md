# Goal

The goal of this challenge is to `create a simple API in Python` that, for a provided geometry, searches a Sentinel-2 satellite scene and computes the `average NDVI (Normalized Difference Vegetation Index)` value. The output would be a single NDVI value (e.g. 0.72) representing the mean NDVI value of that image. The provided geometry (see page 2) is an agricultural area at the river Mosel. You can think of this solution as a simple way to assess the vegetation health of this area.


### Tasks

 - [ ] Implement your solution in `Python 3.x`.
 - [ ] Use the [Element 84 Earth Search API](https://www.element84.com/earth-search/) to search and fetch the Sentinel-2 imagery (library suggestions: requests, rasterio). The selected Sentinel-2 scene should be the most recent scene that covers the geometry, with a cloud cover below 40%.
 - [ ] Implement a method to compute the `average NDVI` value.
 - [ ] Implement at least `3 unit tests` for your code. 
 - [ ] Provide your solution as a `simple API` (e.g. using [FastAPI](https://fastapi.tiangolo.com/)) that outputs the `average NDVI` value.
 - [ ] Provide a `README` with instructions on how to set up, run and test your solution.
 - [ ] Think about `project structure, code quality and Python best practices`.
 - [ ] Submit your solution as a `git project` in a ZIP file.

### Bonus Tasks

 - [ ] Make use of the `Cloud Optimized Geotiff` format to fetch and calculate the NDVI value only for the pixels over the provided geometry instead of the full image.
 - [ ] Implement additional `unit tests` that mock the SAT-API response.
 - [ ] Perform async requests into the `Element84 API`.

## Folder structure

``` text
 tree .
.
├── assets
│   └── map.geojson
├── fastAPI
│   ├── __init__.py
│   ├── main.py
│   └── ndvi.py
├── test
│   └── test_main.py
├── trash
│   └── NDVI_COG.ipynb
├── Dockerfile
├── README.md
└── environment.yml
```

## Result

For this exercise, `3 Endpoints` were created.
The first of these is a simple proof of concept (using GET).
The other two generate the requested result but with `GET` and `POST`, giving the option to experiment with a geojson both as a file and as direct code.


## Installation

In order to make use of the challenge script, a `Dockerfile` has been created so that it can be run on any device.

For this we must first:

```bash
git clone https://github.com/diegoalarc/fastAPI_up42.git

cd fastAPI_up42/
```

To run the application:

```bash
docker build -t challenge .

docker run -d --name mycontainer -p 80:80 challenge
```

And finally visit:

```bash
http://0.0.0.0/docs
```
and try the Endpoints.

### Endpoints description

For this project 3 Endpoints were generated, which are:

1. We have `"/"` as the default Endpoint with greetings to everyone in UP42.
2. We have `"/mean_ndvi_wg"` which is a `GET` that will deliver the requested average. In this we have by default the conditions of the challenge.
3. We have `"/mean_ndvi_wp"` which is a `POST` that will give us the requested average. In this one we have by default most of the conditions of the challenge except for the geometry, which is in the `assets` folder with the name `map.geojson` and must be loaded in the Endpoint.

## Testing

For this purpose, the pytest package was used. The test files are localed inside the tests folder. Here an example of how to run a them:

We need to modify the Dockerfile as follow:

```bash
FROM mambaorg/micromamba:1.2.0

# Set the current working directory to /code.
#This is where we'll put the environment.yml file and the fastAPI directory.
WORKDIR /code

# Copy the file with the requirements to the /code directory.
COPY ./environment.yml /code/environment.yml

RUN micromamba create --name api_up42 --yes --file /code/environment.yml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Activate env
ENV PATH /opt/conda/envs/api_up42/bin:$PATH

EXPOSE 80

# Copy fastAPI testing folder
COPY ./test /code/app

WORKDIR /code/app

# Set the command to run the test using pytest.
CMD python -m pytest
```
and build a new container as:

```bash
docker build -t test .

docker run -d --name mycontainer -p 80:80 test
```
