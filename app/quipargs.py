import argparse

parser = argparse.ArgumentParser(description="QuIP results loader.")
# MONGODB
parser.add_argument("--dbhost", default="localhost", metavar="<hostname>", type=str, help="FeatureDB host name. Default: localhost")
parser.add_argument("--dbport", default=27017, type=int, metavar="<port>", help="FeatureDB host port. Default: 27017")
parser.add_argument("--dbname", required=True, metavar="<name>", type=str, help="FeatureDB database name.")
# PATHDB
parser.add_argument("--pathdb", help="use this flag if pathdb", action="store_true")
parser.add_argument("--url", required=False, type=str, metavar="<url>", help="url of pathdb (example: https://quip.bmi.stonybrook.edu)")
parser.add_argument("--user", required=False, type=str, metavar="<user>", help="username (if pathdb)")
parser.add_argument("--passwd", required=False, type=str, metavar="<passwd>", help="password (if pathdb)")
parser.add_argument("--src", required=True, metavar="<src>", type=str, help="location of segmentation results")
parser.add_argument("--collectionname", required=True, metavar="<collectionname>", type=str, help="PathDB collection name")
args = {}
