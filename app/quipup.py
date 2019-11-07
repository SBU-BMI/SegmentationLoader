'''
Update mongo docs
'''
import datetime

from pathdbapi import *
from quipdb import *
import csv
import sys

# Global vars
img = {
    'study': '',
    'subject': '',
    'image': ''
}

MARK = 'mark'
ANALYSIS = 'analysis'

# Args
execution_id = ''
file_location = ''
collection = ''

# Mongo vars
myclient = connect()
mydb = myclient['']

# Pathdb vars
url = ''
token = get_auth_token(url, sys.argv[1], sys.argv[2])

mydate = datetime.datetime.utcnow()


def do_removal(mycol, myquery):
    print('*** Removing docs in ' + mycol.name + '... ***')
    count = mycol.count_documents(myquery)
    if count == 0:
        print('No docs to remove', mycol.name, '; query:', myquery)
    else:
        print('Count', mycol.name, ':', count)
        mydocs = mycol.find(myquery)
        for x in mydocs:
            ret_val = 0
            if mycol.name == ANALYSIS:
                ret_val = check_it(x['image'])
            if mycol.name == MARK:
                ret_val = check_it(x['provenance']['image'])
            if ret_val:
                mycol.delete_one({'_id': x['_id']})


def do_print(mycol, myquery):
    count = mycol.count_documents(myquery)
    if count == 0:
        print('Count', mycol.name, ':', count, '; query:', myquery)
    else:
        print('Count', mycol.name, ':', count)
        mydocs = mycol.find(myquery)
        if mycol.name == ANALYSIS:
            for x in mydocs:
                print_it(x, x['image'])
        if mycol.name == MARK:
            for x in mydocs:
                print_it(x, x['provenance']['image'])


def print_it(doc, x):
    print(doc['_id'], x['slide'], x['imageid'], x['study'], x['subject'])
    check_it(x)


def check_it(x):
    if x['study'] != img['study'] or x['subject'] != img['subject'] or x['imageid'] != img['image']:
        print("\nSomething didn't match up")
        print(x['study'], '!=', img['study'])
        print(x['subject'], '!=', img['subject'])
        print(x['imageid'], '!=', img['image'], '\n')
        return 0
    else:
        return 1


def do_rename(mycol, myquery, val):
    print('*** Renaming execution_id in ' + mycol.name + '... ***')
    count = mycol.count_documents(myquery)
    if count == 0:
        print('No docs to rename', mycol.name, '; query:', myquery)
    else:
        print('Count', mycol.name, ':', count)
    mydocs = mycol.find(myquery)

    if mycol.name == ANALYSIS:
        for x in mydocs:
            ret_val = check_it(x['image'])
            if ret_val:
                mycol.update_one({'_id': x['_id']},
                                 {'$set': {'analysis.execution_id': val, 'provenance.update_date': mydate}})

    if mycol.name == MARK:
        for x in mydocs:
            ret_val = check_it(x['provenance']['image'])
            if ret_val:
                mycol.update_one({'_id': x['_id']},
                                 {'$set': {'provenance.analysis.execution_id': val, 'provenance.update_date': mydate}})


def do_thing(mycol, myquery):
    print('*** do_thing ' + mycol.name + '... ***')
    count = mycol.count_documents(myquery)
    if count == 0:
        print('No docs to do_thing', mycol.name, '; query:', myquery)
    else:
        print('Count', mycol.name, ':', count)
    mydocs = mycol.find(myquery)
    if mycol.name == MARK:
        for x in mydocs:
            ret_val = check_it(x['provenance']['image'])
            if ret_val:
                mycol.update_one({'_id': x['_id']}, {
                    '$set': {'provenance.data_loader': 'quip-segloader', 'provenance.batch_id': 'bf72e8e',
                             'provenance.tag_id': 'a22a94e', 'provenance.submit_date': mydate}})
                # mycol.update_one({'_id': x['_id']}, {'$unset': {'tag_id': ""}})


# Read file
with open(file_location) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count = 1
            continue
        else:
            img['study'] = row[1]
            img['subject'] = row[2]
            img['image'] = row[3]

            id = get_slide_unique_id(token, url, collection, img['study'], img['subject'], img['image'])
            print('id:', id)
            a_query = {'image.slide': id, 'analysis.execution_id': execution_id}
            m_query = {'provenance.image.slide': id, 'provenance.analysis.execution_id': execution_id}
            # do_removal(mydb[ANALYSIS], a_query)
            # do_removal(mydb[MARK], m_query)
            # do_print(mydb[ANALYSIS], a_query)
            # do_print(mydb[MARK], m_query)
            do_rename(mydb[ANALYSIS], a_query, execution_id + '_mark_backup')
            do_rename(mydb[MARK], m_query, execution_id + '_mark_backup')
            # print(a_query)
            # do_thing(mydb[MARK], m_query)

print('DONE.')
