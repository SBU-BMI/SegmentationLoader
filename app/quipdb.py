import datetime
import random

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def connect(dbhost, dbport):
    dburi = "mongodb://" + dbhost + ":" + str(dbport) + "/"
    client = MongoClient(dburi)
    try:
        res = client.admin.command('ismaster')
    except ConnectionFailure:
        print("Server is not available.")
        return None
    return client


def getdb(client, dbname):
    db = client[dbname]
    return db


def check_metadata(db, mdata, pathdb, pdb):
    query = {}
    if pathdb:
        # query["uuid"] = pdb["uuid"]
        query["image.slide"] = str(pdb["slide"])
    else:
        # Keys: slide, specimen, study, execution_id
        query["image.slide"] = str(mdata["case_id"])
        query["image.study"] = ""
        query["analysis.execution_id"] = mdata["analysis_id"]
    query["image.specimen"] = ""  # Specimen currently blank
    res = db.analysis.find_one(query)
    return res


def submit_metadata(db, mdata, pathdb, pdb):
    mdoc = {}
    imgdoc = {}

    # Specimen currently blank
    imgdoc["specimen"] = ""

    if pathdb:
        # mdoc["uuid"] = pdb["uuid"]
        imgdoc["slide"] = str(pdb["slide"])
        imgdoc["imageid"] = str(pdb["imageid"])
        imgdoc["study"] = pdb["study"]
        imgdoc["subject"] = pdb["subject"]
    else:
        imgdoc["slide"] = str(mdata["case_id"])
        imgdoc["study"] = ""
        imgdoc["subject"] = mdata["subject_id"]

    mdoc["image"] = imgdoc
    provdoc = {}
    provdoc["execution_id"] = mdata["analysis_id"]
    provdoc["type"] = "computer"
    provdoc["computation"] = "segmentation"

    # provdoc["algorithm_params"] = mdata
    algparms = {}
    algparms["input_type"] = mdata["input_type"]
    algparms["otsu_ratio"] = mdata["otsu_ratio"]
    algparms["curvature_weight"] = mdata["curvature_weight"]
    algparms["min_size"] = mdata["min_size"]
    algparms["max_size"] = mdata["max_size"]
    algparms["ms_kernel"] = mdata["ms_kernel"]
    algparms["declump_type"] = mdata["declump_type"]
    algparms["levelset_num_iters"] = mdata["levelset_num_iters"]
    algparms["mpp"] = mdata["mpp"]
    algparms["image_width"] = mdata["image_width"]
    algparms["image_height"] = mdata["image_height"]
    algparms["tile_width"] = mdata["tile_width"]
    algparms["tile_height"] = mdata["tile_height"]
    algparms["patch_width"] = mdata["patch_width"]
    algparms["patch_height"] = mdata["patch_height"]
    algparms["output_level"] = mdata["output_level"]
    algparms["subject_id"] = mdata["subject_id"]
    algparms["case_id"] = mdata["case_id"]
    algparms["analysis_id"] = mdata["analysis_id"]
    algparms["analysis_desc"] = mdata["analysis_desc"]
    provdoc["algorithm_params"] = algparms

    provdoc["randval"] = random.random()
    provdoc["submit_date"] = datetime.datetime.utcnow()
    mdoc["analysis"] = provdoc
    res = db.analysis.insert_one(mdoc)


def submit_results(db, results):
    res = db.mark.insert_many(results)
