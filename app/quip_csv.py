"""
Loads wsi segmentations to the database.
"""
import csv
import os
import glob
import json
import random
import sys
import urllib.parse
from multiprocessing import Pool

import quipargs
import quipdb
import requests
from geojson import Point, Polygon

pathdb = False
pdb = {}


def get_file_list(folder):
    '''
    Each folder contains data for segmentation results for 1 wsi.
    This function returns a list of algmeta.json files
    '''
    metafiles = []
    fnames = folder + "/*-algmeta.json"
    i = 1
    for name in glob.glob(fnames):
        metafiles.append((folder, name, i))
        i = i + 1
    return metafiles


def process_quip(mfile):
    '''
    Processes files
    '''
    dir = mfile[0]
    algmeta_json = mfile[1]
    index = mfile[2]
    mdata = read_metadata(algmeta_json)
    process_file(mdata, dir, index)


def read_metadata(meta_file):
    '''
    Decodes JSON file to dictionary
    '''
    mf = open(meta_file)
    data = json.load(mf)
    return data


def process_file(mdata, fname, idx):
    '''
    Creates json and uploads to mongo
    '''
    image_width = mdata["image_width"]
    image_height = mdata["image_height"]
    # print(image_width, image_height)

    fname = fname + "/" + mdata["out_file_prefix"] + "-features.csv"

    csvfile = open(fname)
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)
    polycol = headers.index("Polygon")

    if is_blank(mdata["analysis_id"]):
        print('execution_id cannot be blank. File:', fname)
        sys.exit()

    cnt = 0
    multi_documents = []
    for row in csvreader:
        polydata = row[polycol]
        polyjson, corners, bounding_box = poly_geojson(polydata.split(":"), image_width, image_height)

        if polyjson is None:
            print('PLEASE FIX FILE!', fname)
            return

        name = mdata["analysis_id"]

        scfeatures = {}
        scfeatures["annotations"] = set_scalar_features(row, headers, polycol, name)

        # Geometries
        geo_collection = {}
        geo_collection["type"] = "FeatureCollection"

        object = {}
        object["type"] = "Feature"
        object["properties"] = {
            "style": {
                "color": "#00fcfc",
                "lineJoin": "round",
                "lineCap": "round",
                "isFill": False
            },
            "nommp": True
        }
        object["geometry"] = polyjson
        object["bound"] = Polygon(bounding_box)

        features = []
        features.append(object)
        geo_collection["features"] = features

        gj_poly = {}
        # if pathdb:
        #     gj_poly["uuid"] = uuid
        gj_poly["properties"] = scfeatures
        gj_poly["geometries"] = geo_collection
        gj_poly["footprint"] = float(row[headers.index("AreaInPixels")])

        set_document_metadata(gj_poly, corners, mdata, "b0", "t0", name)
        multi_documents.append(gj_poly)
        cnt = cnt + 1
    print("IDX: ", idx, " File: ", fname, "  Count: ", cnt)

    if cnt > 0:
        dbhost = quipargs.args["dbhost"]
        dbport = quipargs.args["dbport"]
        dbname = quipargs.args["dbname"]
        myclient = quipdb.connect(dbhost, dbport)
        mydb = quipdb.getdb(myclient, dbname)
        quipdb.submit_results(mydb, multi_documents)
        res = quipdb.check_metadata(mydb, mdata, pathdb, pdb)
        if res is None:
            quipdb.submit_metadata(mydb, mdata, pathdb, pdb)
        myclient.close()


def poly_geojson(polydata, imw, imh):
    '''
    Returns Polygon object; coordinates and bounding box.
    '''
    polyarray = []
    found = False

    try:
        x1 = float(polydata[0].split("[")[1]) / float(imw)
        y1 = float(polydata[1]) / float(imh)
    except ValueError:
        print('Non-numeric data found in the file.', polydata[0], polydata[1])
        # val.isalpha() will not work on '[' or ']'
        if "[" in polydata[0]:
            val = polydata[0].replace('[', '')  # Hiccup.
            x1 = float(val) / float(imw)
        if "]" in polydata[1]:
            val = polydata[1].replace(']', '')  # Hiccup.
            y1 = float(val) / float(imh)
        print('Fixed.')

    minx = x1
    miny = y1
    maxx = x1
    maxy = y1
    polyarray.append((x1, y1))
    i = 2
    try:
        while i < len(polydata) - 2:
            if found:
                if "[" in polydata[i]:
                    val = polydata[i].replace('[', '')
                    x = float(val) / float(imw)
                if "]" in polydata[i + 1]:
                    val = polydata[i + 1].replace(']', '')
                    y = float(val) / float(imh)
            else:
                x = float(polydata[i]) / float(imw)
                y = float(polydata[i + 1]) / float(imh)
            if minx > x:
                minx = x
            if miny > y:
                miny = y
            if maxx < x:
                maxx = x
            if maxy < y:
                maxy = y
            polyarray.append((x, y))
            i = i + 2
        x = float(polydata[i]) / float(imw)
        y = float(polydata[i + 1].split("]")[0]) / float(imh)
        if minx > x:
            minx = x
        if miny > y:
            miny = y
        if maxx < x:
            maxx = x
        if maxy < y:
            maxy = y
    except IndexError as e:
        print('Had some trouble making this polygon', polydata, e)
        return None, None, None

    polyarray.append((x, y))
    polyarray.append((x1, y1))
    corners = [minx, miny, maxx, maxy]

    min_point = Point((minx, miny))  # smallest x and y value
    mid_point = Point((minx, maxy))
    max_point = Point((maxx, maxy))  # largest x and y value.
    m1d_point = Point((maxx, miny))
    # min_point = Point((minx, miny))  # closes the loop
    my_array = [[min_point, mid_point, max_point, m1d_point, min_point]]
    bounding_box = Polygon(my_array)

    return Polygon([polyarray]), corners, bounding_box


def set_scalar_features(row, headers, polycol, name):
    '''
    Create name:value pairs (json) to be loaded to database
    '''
    scalar_values = {}
    # Assuming polycol is last column
    for i in range(polycol):
        scalar_values[headers[i]] = float(row[i])
    scalar_values["ns"] = "http://u24.bmi.stonybrook.edu/v1"
    scalar_values["name"] = name
    return scalar_values


def set_provenance_metadata(mdata, batch_id, tag_id, name, pathdb, pdb):
    # IMAGE
    image = {}
    if pathdb:
        image["slide"] = str(pdb["slide"])
        image["imageid"] = pdb["imageid"]
        image["study"] = pdb["study"]
        image["subject"] = pdb["subject"]
    else:
        image["slide"] = mdata["case_id"]
        image["imageid"] = mdata["case_id"]
        image["study"] = ''
        image["subject"] = mdata["subject_id"]

    image["specimen"] = ''  # Specimen currently blank

    # ANALYSIS
    analysis = {}
    analysis["source"] = "computer"
    analysis["execution_id"] = mdata["analysis_id"]
    analysis["name"] = name
    analysis["computation"] = "segmentation"

    provenance = {}
    provenance["image"] = image
    provenance["analysis"] = analysis
    provenance["data_loader"] = "0.99"
    provenance["batch_id"] = batch_id
    provenance["tag_id"] = tag_id
    return provenance


def set_document_metadata(gj_poly, bbox, mdata, batch_id, tag_id, name):
    gj_poly["parent_id"] = "self"
    gj_poly["normalized"] = "true"
    gj_poly["bbox"] = bbox
    gj_poly["x"] = (float(bbox[0]) + float(bbox[2])) / 2
    gj_poly["y"] = (float(bbox[1]) + float(bbox[3])) / 2
    gj_poly["object_type"] = "nucleus"
    gj_poly["randval"] = random.random()
    gj_poly["provenance"] = set_provenance_metadata(mdata, batch_id, tag_id, name, pathdb, pdb)


def get_auth_token():
    '''
    get an auth token
    '''
    endpoint = pdb["url"] + '/jwt/token'
    response = requests.get(endpoint, auth=(pdb["user"], pdb["passwd"]))
    if response.status_code == 403:
        raise MyException('Error getting token. status_code was: {}'.format(response.status_code))
    else:
        response = response.json()
        token_string = response['token']

    return token_string


def get_slide_unique_id(collection, studyid, clinicaltrialsubjectid, imageid):
    # Get token
    token = get_auth_token()

    # COLLECTION/STUDY/SUBJECT/IMAGE
    coll_encoded = urllib.parse.quote(collection)

    # NEW WAY
    endpoint = pdb["url"] + "/idlookup/" + coll_encoded + "/" + studyid + "/" + clinicaltrialsubjectid + "/" + imageid
    # OLD WAY
    # endpoint = pdb["url"] + "/idlookup/" + studyid + "/" + clinicaltrialsubjectid + "/" + imageid + "/" + coll_encoded
    # print('endpoint', endpoint)

    headers = {"Authorization": "Bearer " + token}
    response = requests.get(endpoint, headers=headers).json()
    if response:
        # pdb["uuid"] = response[0]['uuid'][0]['value']
        pdb["slide"] = response[0]['nid'][0]['value']
        print('slide id', pdb["slide"])
    else:
        print('Error getting ID.', response)
        print('endpoint', endpoint)
        exit(1)

    return str(pdb["slide"])


def is_blank(myString):
    if myString and myString.strip():
        # myString is not None AND myString is not empty or blank
        return False
    # myString is None OR myString is empty or blank
    return True


def check_args_pathdb(args):
    if not args['user'] or not args['passwd'] or not args['collectionname']:
        print("dependency error")
        print("when in pathdb mode, must provide: url, username, and password")
        exit(1)
    pdb["collection"] = args["collectionname"]
    pdb["url"] = args["url"]
    pdb["user"] = args["user"]
    pdb["passwd"] = args["passwd"]
    pdb["slide"] = ""
    # pdb["uuid"] = ""


class MyException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


if __name__ == "__main__":
    quipargs.args = vars(quipargs.parser.parse_args())
    pathdb = quipargs.args["pathdb"]

    random.seed(a=None)
    csv.field_size_limit(sys.maxsize)

    if pathdb:
        check_args_pathdb(quipargs.args)

    dirpath = os.path.join('/data', quipargs.args['src'])
    manifest = os.path.join(dirpath, 'manifest.csv')
    print('dirpath', dirpath)
    print('manifest', manifest)
    if not os.path.exists(manifest):
        print('Manifest file not found:', manifest)
        exit(1)

    with open(manifest) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            file_loc = os.path.join(dirpath, row[0])

            if not os.path.exists(file_loc):
                print('File location not found:', file_loc)
                exit(1)

            if pathdb:
                pdb["study"] = row[1]
                pdb["subject"] = row[2]
                pdb["imageid"] = row[3]

                try:
                    _id = get_slide_unique_id(pdb["collection"], pdb["study"], pdb["subject"], pdb["imageid"])
                    if is_blank(_id):
                        print('Slide not found ' + pdb["imageid"])
                        exit(1)
                except MyException as e:
                    details = e.args[0]
                    print(details)
                    exit(1)

            mfiles = get_file_list(file_loc)
            p = Pool(processes=2)
            p.map(process_quip, mfiles, 1)
