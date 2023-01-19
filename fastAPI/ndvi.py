#ndvi.py

import copy
import numpy as np
import rasterio as rio
from satsearch import Search
from pyproj import Transformer

transform_window = None

def range_request(image_url, bbox):
    """
    Request and read the required pixels from the COG image
    """
    
    with rio.open(image_url) as src:
        coord_transformer = Transformer.from_crs("epsg:4326", src.crs)
        # Calculate pixels to be streamed from the COG
        coord_upper_left = coord_transformer.transform(bbox[3], bbox[0])
        coord_lower_right = coord_transformer.transform(bbox[1], bbox[2])
        pixel_upper_left = src.index(coord_upper_left[0], coord_upper_left[1])
        pixel_lower_right = src.index(coord_lower_right[0], coord_lower_right[1])
         
                
        # Request only the bytes in the window
        window = rio.windows.Window.from_slices(
            (pixel_upper_left[0], pixel_lower_right[0]),
            (pixel_upper_left[1], pixel_lower_right[1]),
        )

        # The affine transform - This will allow us to 
        # translate pixels coordiantes back to geospatial coordiantes
        transform_window = rio.windows.transform(window,src.transform)
        
        bands = 1

        # True Colour Image aka RGB
        if "TCI" in image_url:
            bands = [1, 2, 3]

        subset = src.read(bands, window=window)
        return(subset, transform_window)

def image_search(bbox, date_range, scene_cloud_tolerance):
    """
    Using SatSearch find all Sentinel-2 images
    that meet our criteria
    """
    
    search = Search(
        bbox = bbox,
        datetime = date_range,
        query = {
            "eo:cloud_cover": {"lt": scene_cloud_tolerance}
        },
        collections = ["sentinel-s2-l2a-cogs"],
        # Sentinel-2 STAC API
        url = "https://earth-search.aws.element84.com/v0/",
    )

    return search.items()

def is_cloudy(scl, tolerance):
    """
    Calculate the cloud cover in the subset-scene
    """
    
    image_size = scl.size
    unique, count = np.unique(scl, return_counts=True)
    counts = dict(zip(unique, count))

    # Sum cloud types
    cloud_med_probability = counts.get(8, 0)
    cloud_high_probability = counts.get(9, 0)
    thin_cirrus = counts.get(10, 0)
    total_cloud_cover = cloud_med_probability + cloud_high_probability + thin_cirrus  
    
    # Percent subscene cloud cover
    percent_cloud_cover = 100 * float(total_cloud_cover) / float(image_size)
    if percent_cloud_cover > tolerance:
        return True
    return False

def ndvi_mean(bbox, date_range, scene_cloud_tolerance):
    """
    Compute the average NDVI value
    """
    images= []

    # Percentage of clouds in the subscene (AOI COG image)
    subset_scene_cloud_tolerance = 2

    items = image_search(bbox, date_range, scene_cloud_tolerance)
    for item in items:
        
        # Refs to images
        red = item.asset("red")["href"]
        nir = item.asset("nir")["href"]
        scl = item.asset("SCL")["href"]
        date = item.date.strftime("%d/%m/%Y")
        
        # Check for clouds in sub-scene before continuing 
        if subset_scene_cloud_tolerance:
            scl_subset, transform_window = range_request(scl, bbox)
            if is_cloudy(scl_subset, subset_scene_cloud_tolerance) == 0:

                # Streamed pixels within bbox
                red_subset, transform_window = range_request(red, bbox)
                nir_subset, transform_window = range_request(nir, bbox)

                # Calcualte NDVI
                ndvi_subset = (nir_subset.astype(float) - red_subset.astype(float)) / (
                    nir_subset + red_subset
                )

                # Calculate NDVI mean
                ndvi_gtpt0 = copy.copy(ndvi_subset)
                # Set all pixels with NDVI < 0 to nan, keeping only values > 0
                ndvi_gtpt0[ndvi_subset<0] = np.nan
                mean_NDVI = round(np.nanmean(ndvi_gtpt0),2)

                # Store the data for further processing
                images.append(
                    {"Average NDVI value": mean_NDVI, "Image date": date}
                    )

                break

            else:

                continue
    
    return images