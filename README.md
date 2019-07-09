# quip_segmentation_loader
Load WSI segmentations to mongodb instance in a Docker network environment (i.e. QuIP).

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

Map your local segmentation results directory to container directory `/data/segmentation_results`.

To find out what network:
```
docker inspect ca-mongo -f "{{json .NetworkSettings }}"
```
Use that information in place of `distro_default` above.

## Usage
### PathDB

```
docker exec seg-loader /app/loadfiles.sh <dbhost> <dbport> <dbname> <url> <username> <password> <manifest.csv>
```

