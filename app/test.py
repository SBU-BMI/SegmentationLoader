from pathdbapi import *
import sys

token = get_auth_token(sys.argv[1], sys.argv[2], sys.argv[3])
print(token)

id = get_slide_unique_id(token, sys.argv[1], "TCGA BRCA DEMO", "TCGA-BRCA", "TCGA-A2-A3XZ", "A3XZ-01Z-00-DX1")
print(id)

# raise MyException("My hovercraft is full of eels")
