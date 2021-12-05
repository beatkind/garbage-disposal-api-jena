import flask
from flask import request, jsonify, abort
import logging
import csv

format = '%(asctime)s: %(message)s'
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

logging.info('gdaj started...')
logging.info('Doing init stuff...')

app = flask.Flask(__name__)
api_base = '/api/v1'

logging.info('App started...')


@app.route('/', methods=['GET'])
def home():
    return '<h1> GDAJ - garbage disposal api jena</h1>'


@app.route(api_base + '/getby_street', methods=['GET'])
def getby_street():
    if 'street' in request.args:
        street = str(request.args['street'])
    else:
        street = ''
    if 'house_number' in request.args:
        house_number = str(request.args['house_number'])
    else:
        house_number = ''
    if 'garbage_type' in request.args:
        garbage_type = str(request.args['garbage_type'])
    else:
        garbage_type = ''

    logging.info('Request: ' + street + ' ' + house_number + ' ' + garbage_type)

    result = {}

    with open('entsorgungstermine.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[2] == street and row[3] == house_number and garbage_type == '':
                    result[(str(row[1]))] = row[12], row[13]
                    line_count += 1
                elif row[2] == street and row[3] == house_number and garbage_type == row[1]:
                    result[(str(row[1]))] = row[12], row[13]
                    break

    logging.info('Return: ' + str(result))

    return jsonify(result)
