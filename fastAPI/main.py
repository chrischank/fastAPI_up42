# main.py

# Sources:
# https://github.com/sat-utils/sat-search
# https://github.com/henriod/fastApi_sentinel
#https://www.simonplanzer.com/articles/cog-ndvi-part1/
# https://github.com/cristianmurillo87/ndvi-cog-catalog
# https://stacspec.org/en/tutorials/access-sentinel-2-data-aws/
# https://pythonawesome.com/how-to-use-cogs-cloud-optimized-geotiffs-with-rasterio/

# Libraries
import uvicorn
import geojson
import geopandas as gpd
from ndvi import *
from shapely.geometry import shape
from fastapi import FastAPI, UploadFile, HTTPException

description = """
## UP42 Geospatial Engineering Challenge 🚀

The goal of this challenge is to create a simple API in Python that, for a provided geometry, searches a Sentinel-2 satellite scene and computes the average NDVI (Normalized Difference Vegetation Index) value.

### Result

For this exercise, 3 Endpoints were created.
The first of these is a simple proof of concept (using GET).
The other two generate the requested result but with GET and POST, giving the option to experiment with a geojson both as a file and as direct code.
"""


app = FastAPI(
    title = "UP42 Challenge",
    description = description,
    version = "0.0.1",
    contact = {
        "name": "Diego Alarcón",
        "url": "https://diegoalarc.github.io/",
        "email": "diego.alarcondiaz@gmailcom",
    },
    swagger_ui_parameters = {"defaultModelsExpandDepth": -1}
)

# Default Endpoint with greetings for everyone at UP42
@app.get("/", tags = ["Endpoints"])
async def greetings():
   return {"message": "Greetings to everyone at UP42!!!!"}

"""
We are Using get Method

Endpoint function to obtain the average ndvi when provide with
@Geojson feature as explicit geojson file
@date_range = "YYYY-MM-dd/YYYY-MM-dd"
@scene_cloud_tolerance = int
The script check if file is valid (geojson geometry is either Polygon or multipolygon) and if data can be calculated.
/mean_ndvi_wg = mean ndvi with post
"""

@app.get("/mean_ndvi_wg", tags = ["Endpoints"])
async def get_mean_ndvi(
 
   # Bounding Box delineating the spatial extent for NDVI mapping
    Geojson_feature: str = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [7.163171768188476,50.01584714780868],
                        [7.1739864349365225,50.01584714780868],
                        [7.1739864349365225,50.01970768279515],
                        [7.163171768188476,50.01970768279515],
                        [7.163171768188476,50.01584714780868]
                        ]]
                        }
                    }
                ]
            },
 
   # The date range for mapping NDVI overtime
   Date_range: str = "2022-11-01/2023-01-10",
 
   # Cloud cover tolerance
   Cloud_tolerance: int = 40
 
):
 
    try:
        # Converting to bbox
        geojson_object = geojson.loads(Geojson_feature)

    except:
        raise HTTPException(
            status_code = 404,
            detail = "The data could not be converted to bbox"
            )
    
    # Validation geojson
    if geojson_object.is_valid:

        # Geometry from object
        geometry = geojson_object['features'][0]['geometry']

        # Convert to shapely object
        geom = shape(geometry)

        # Get bounding box
        bbox = geom.bounds

        # Funtion to calculated average NDVI from COG image
        return ndvi_mean(bbox, Date_range, Cloud_tolerance)
        
    raise HTTPException(
        status_code = 404,
        detail = "The data could not be calculated"
        )


"""
We are Using post Method

Endpoint function to obtain the average ndvi when provide with
@Geojson feature as loadable geojson file
@date_range2 = "YYYY-MM-dd/YYYY-MM-dd"
@scene_cloud_tolerance2 = int
The script check if file is valid (geojson geometry is either Polygon or multipolygon) and if data can be calculated.
/mean_ndvi_wp = mean ndvi with post
"""

@app.post("/mean_ndvi_wp", tags = ["Endpoints"])
async def get_mean_ndvi(
 
   # Bounding Box delineating the spatial extent for NDVI mapping
   Geojson_file: UploadFile,
 
   # The date range for mapping NDVI overtime
   Date_range: str = "2022-11-01/2023-01-10",
 
   # Cloud cover tolerance
   Cloud_tolerance: int = 40
 
):
    try:
        # Read geojson
        # with open(Geojson_file.file) as f:
        #     polygons_gdf = geojson.load(f)

        polygons_gdf = gpd.read_file(Geojson_file.file)

        geo_shapes = []

        # Get geometry values in a list
        for geo_shape in polygons_gdf.geometry.values:
            geo_shapes.append(geo_shape)
    
    except:
        raise HTTPException(
            status_code = 404,
            detail = "The data could not be converted to bbox"
            )

    # Boolean validation list values
    if geo_shapes[0].is_valid:

        # Convert to shapely object
        geom = shape(geo_shapes[0])

        # Get bounding box
        bbox = geom.bounds

        # Funtion to calculated average NDVI from COG image
        return ndvi_mean(bbox, Date_range, Cloud_tolerance)
    
    raise HTTPException(
       status_code = 404,
       detail = "The data could not be calculated"
       )

# Activate unicorn server to run API
# http://127.0.0.1:8000/docs#/
if __name__ == '__main__':
   uvicorn.run("main:app",reload = True)