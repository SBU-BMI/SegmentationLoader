# SegmentationLoader
Load WSI segmentations to mongodb instance in a Docker network environment (i.e. QuIP).

Loading segmentations:

Segmentation results to be loaded to PathDB should be put in the `segmentation_results` folder in the QuIP main data folder. This folder must contain the appropriate manifest file.

Running the following as a background process is recommended.

Example:
```
nohup docker exec quip-segloader /app/loadfiles.sh username password &  
```
