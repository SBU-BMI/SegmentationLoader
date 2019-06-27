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
        query["slide"] = pdb["slide"]
    else:
        # Keys: slide, specimen, study, execution_id
        query["image.slide"] = mdata["case_id"]
        query["image.specimen"] = ""  # Specimen currently blank
        query["image.study"] = ""
        query["analysis.execution_id"] = mdata["analysis_id"]
    res = db.analysis.find_one(query)
    return res


def submit_metadata(db, mdata, pathdb, pdb):
    mdoc = {}
    imgdoc = {}

    # Specimen currently blank
    imgdoc["specimen"] = ""

    if pathdb:
        # mdoc["uuid"] = pdb["uuid"]
        imgdoc["slide"] = pdb["slide"]
        imgdoc["imageid"] = pdb["imageid"]
        imgdoc["study"] = pdb["study"]
        imgdoc["subject"] = pdb["subject"]
        # imgdoc["study"] = pdb["imageid"]
        # imgdoc["subject"] = pdb["imageid"]
    else:
        imgdoc["slide"] = mdata["case_id"]
        imgdoc["study"] = ""
        imgdoc["subject"] = mdata["subject_id"]

    mdoc["image"] = imgdoc
    provdoc = {}
    provdoc["execution_id"] = mdata["analysis_id"]
    provdoc["type"] = "computer"
    provdoc["computation"] = "segmentation"
    provdoc["algorithm_params"] = mdata
    provdoc["randval"] = random.random()
    provdoc["submit_date"] = datetime.datetime.utcnow()
    mdoc["analysis"] = provdoc
    res = db.analysis.insert_one(mdoc)


def submit_results(db, results):
    res = db.mark.insert_many(results)
