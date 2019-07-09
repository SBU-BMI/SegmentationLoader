# quip\_segmentation\_loader
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

### manifest.csv
This file will be passed as an argument to the program.  See manifest.csv for further details.
Putting this file in the mapped local directory (`~/data/segmentation_results`, above) is recommended.

`path` should be relative to the docker container.
Example: /data/segmentation_results/WSI_FOLDER_NAME

## Usage
Running the following as a background process is recommended.

### PathDB

```
docker exec seg-loader /app/loadfiles.sh <dbhost> <dbport> <dbname> <url> <username> <password> <manifest.csv>
```
### camic
```
docker exec seg-loader /app/loadfiles.sh <dbhost> <dbport> <dbname> <manifest.csv>
```

### Note: 

For non-PathDB usage, the manifest.csv file **will** be used for file location.<br>
`collection` is irrelevant, so it won't be used.<br>
`subject` field will be retrieved from the segmentation data `mdata["subject_id"]`.<br>
`study` will be blank.<br>
`slide` and `imageid` will be set to `mdata["case_id"]`.
