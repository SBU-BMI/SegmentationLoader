import argparse

parser = argparse.ArgumentParser(description="QuIP results loader.")
parser.add_argument("--dbhost", default="localhost", metavar="<hostname>", type=str, help="FeatureDB host name. Default: localhost")
parser.add_argument("--dbport", default=27017, type=int, metavar="<port>", help="FeatureDB host port. Default: 27017")
parser.add_argument("--dbname", required=True, metavar="<name>", type=str, help="FeatureDB database name.")
parser.add_argument("--quip", required=True, type=str, metavar="<folder>", help="QuIP results folder name.")
parser.add_argument("--pathdb", help="use this flag if pathdb", action="store_true")
parser.add_argument("--url", required=False, type=str, metavar="<url>", help="url of pathdb (example: https://quip.bmi.stonybrook.edu)")
parser.add_argument("--collection", required=False, type=str, metavar="<collection>", help="name of collection")
parser.add_argument("--study", required=False, type=str, metavar="<study id>", help="study id")
parser.add_argument("--subject", required=False, type=str, metavar="<subject id>", help="subject id")
parser.add_argument("--prefix", required=False, type=str, metavar="<slide name substitution>", help="slide name subsubstitution")
parser.add_argument("--user", required=False, type=str, metavar="<user>", help="username (if pathdb)")
parser.add_argument("--passwd", required=False, type=str, metavar="<passwd>", help="password (if pathdb)")

args = {}
