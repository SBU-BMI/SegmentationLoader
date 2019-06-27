# quip_segmentation_loader
Load WSI segmentations to mongodb instance
## Usage

### Main Program
quip_csv.py loads a set of input files to the database

### Parameters
The following arguments are required:

```
--dbname (database name)
--quip	 (path to data folder)
```

Default arguments:

```bash
--dbhost	localhost
--dbport	27017
```

Optional argument:

```bash
--pathdb
```

Dependency arguments:

The --pathdb argument requires the --url, --user, and --passwd

```
--url			pathdb (example: https://quip.bmi.stonybrook.edu)
--collection	name of collection
--study		study id
--subject       subject id
--user		username
--passwd	password
--prefix    slide name substitution
            DICOM standard is 16 chars.  Typically, slide name will be truncated 0-16.
            However, if the name has a non-identifying prefix, the prefix you specify will be removed.
```

If you want to check the parameters, you could always do this:
```bash
python quip_csv.py -h
```
## Data

### Input Files

**Features CSV**

Naming convention is: name-features.csv

Header will contain feature names, and `Polygon` is last column.

Polygon field must be last column, in format:
```
[float:float:float:float:float]
```

**Metadata JSON**

For every feature csv, there is a metadata json file.

Naming convention is: name-algmeta.json
