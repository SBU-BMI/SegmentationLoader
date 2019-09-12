# SegmentationLoader
Load WSI segmentations to mongodb instance in a Docker network environment (i.e. QuIP).

Loading segmentations:

<!--
Segmentation results to be loaded to PathDB must reside in a subfolder within the QuIP main data folder. This subfolder must contain the appropriate manifest file.
-->

Running the loader as a **background process** is highly recommended.

Example command:

```
nohup docker exec quip-segloader loadfiles --src [data_folder] --collectionname [pathdb collection] --user [username] --passwd [password] &
```

Regarding --src [data_folder]:<br>
See directory structure of ./data for example<br>
In this case, the folder name you would pass to the program is `brca`.<br>
Also note the manifest.csv file location.

### Build
docker-compose.yml included for convenience

Edit the file and edit `volumes` - set the source to your main data folder.

Currently, source is set to `./data`

If your network name should change (<u>Hint:</u> it shouldn't!) then change `networks` as well.

### Note
This application is based on the premise that the folder name is the same as the SVS file name.  ie. TCGA-XX-XXXX-XXX-XX-XXX.svs should be what goes into the manifest under "segmentdir".
This project is a work in progress.
