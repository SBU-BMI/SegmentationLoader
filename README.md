# SegmentationLoader
Load WSI segmentations to mongodb instance in a Docker network environment (i.e. QuIP).

## Setup
### Folder Structure
See directory structure of ./data:

```
├── data
│   ├── brca
│       ├── segmented files 
|       ├── ...lots of segmented files
│   ├── manifest.csv
```

The manifest file will on the same level as the directory that contains 
 
### Manifest file
Segmentation data is one folder per slide.  So in the <a href="https://github.com/SBU-BMI/SegmentationLoader/blob/master/data/brca/manifest.csv">manifest.csv</a> file, you'll have:

```
datadir    studyid    clinicaltrialsubjectid    imageid
```

## Usage
### Loading segmentations:

Running the loader as a <span style="background-color: #FFFF00">background process</span> is highly recommended.

Example command:

```
nohup docker exec quip-segloader loadfiles --src [data_folder] --collectionname [pathdb collection] --user [username] --passwd [password] &
```

data_folder = folder containing data subfolder and manifest.csv
The upper level directory (/data) is the folder that is mapped to docker.
In this example, the folder name you would pass to the program is `brca`.<br>
Also note the manifest.csv file location.


### Build
docker-compose.yml included for convenience

Edit the file and edit `volumes` - set the source to your main data folder.

Currently, source is set to `./data`

If your network name should change (<u>Hint:</u> it shouldn't!) then change `networks` as well.
