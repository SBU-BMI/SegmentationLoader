# SegmentationLoader
Load WSI segmentations to mongodb instance in a Docker network environment (i.e. QuIP).

Loading segmentations:

Segmentation results to be loaded to PathDB must reside in a subfolder within the QuIP main data folder. This subfolder must contain the appropriate manifest file.

Running the following as a background process is recommended.

Example:

```
nohup docker exec quip-segloader loadfiles --src [data subfolder] --collectionname [pathdb collection] --user [username] --passwd [password] &  
```
