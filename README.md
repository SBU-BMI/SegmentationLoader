# quip_segmentation_loader
Load WSI segmentations to mongodb instance

## Build

```
git clone https://github.com/SBU-BMI/quip_segmentation_loader.git
cd quip_segmentation_loader
docker build --tag segmentation_loader .
```

## Run
Example:

```
docker run --name seg-loader --network distro_default -v ~/data/segmentation_results:/data/segmentation_results -itd segmentation_loader
```

## Usage
### PathDB

```
nohup docker exec seg-loader /app/loadfiles.sh <pathdb-url> <collection> <study> <subject> <username> <password> &
```
(Recommend running load script in background)

<!-- See: [Docker repository](https://hub.docker.com/r/sbubmi/segmentation_loader/). -->

### TBD
