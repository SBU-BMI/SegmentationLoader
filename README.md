# SegmentationLoader
Load WSI segmentations to mongodb instance in a Docker network environment (i.e. QuIP).
<!-- docker run --name quip-segloader --network distro_default -v ~/data/segmentation_results:/data/segmentation_results -itd quip_distro_segloader -->

## Setup
### Folder Structure
See  **<a href="./tree/master/data">EXAMPLE</a>**.

Directory structure of ./data:

```
├── data/
│   ├── segmentation_results/
|       ├── manifest.csv
│       ├── TCGA-A2-A3XZ-01Z-00-DX1.svs/ (folder)
|           ├── ...lots of segmented files
|
```

The manifest file will on the same level as the directory that contains 
 
### Manifest file
Segmentation data is one folder per slide.  So in the **<a href="./blob/master/data/segmentation_results/manifest.csv">manifest.csv</a>** file, you may have, for example:

```
segmentdir,studyid,clinicaltrialsubjectid,imageid
TCGA-A2-A3XZ-01Z-00-DX1.svs,TCGA-A2-A3XZ-01Z,TCGA-A2-A3XZ-01Z-00-DX1,TCGA-A2-A3XZ-01Z
```

## Example Usage
### Loading segmentations:

Running the loader as a <span style="background-color: #FFFF00">background process</span> is highly recommended.

```
# Command with arguments:
nohup docker exec quip-segloader loadfiles --src [data_folder] --collectionname [pathdb collection] --user [username] --passwd [password] > /dev/null &

# Example:
nohup docker exec quip-segloader loadfiles --src segmentation_results --collectionname TCGABRCA --user [your username] --passwd [your password] > /dev/null &

```

The `> /dev/null &` is for keeping any error logs that may occur, but not generate any other output files (so as to not eat up all the space).

data_folder = top-level directory containing segmentation subfolder and manifest.csv

FYI, the upper level directory (in this case, `./data`) is the folder that is mapped to docker.

In this example, the folder name you would pass to the program is `segmentation_results`.


### Build
`docker-compose.yml` included for convenience

Edit the file and edit `volumes` - set the source to your main data folder.

Currently, source is set to `./data`

If your network name should change (<u>Hint:</u> **it shouldn't**) but if it does, then change `networks` as well.
