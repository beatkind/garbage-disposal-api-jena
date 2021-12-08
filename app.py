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

logging.info('App started...')


@app.route('/', methods=['GET'])
def home():
    return '<h1> GDAJ - garbage disposal api jena</h1>'


@app.route('/getby_street', methods=['GET'])
def getby_street():
    if 'street' in request.args:
        street = str(request.args['street']).lower()
    else:
        street = ''
    if 'house' in request.args:
        house_number = str(request.args['house']).lower()
    else:
        house_number = ''
    if 'garbage_type' in request.args:
        garbage_type = str(request.args['garbage_type']).lower()
    else:
        garbage_type = ''

    logging.info('Request - ' + str(request.user_agent) + ': ' +
                 street + ' ' + house_number + ' ' + garbage_type)

    result = {}
    day = {}
    week = {}

    with open('entsorgungstermine.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                
                csv_garbage = row[1].lower()
                csv_street = row[2].lower()
                csv_house = row[3].lower()
                
                if csv_street == street and csv_house == house_number and garbage_type == '':
                    result[(str(row[1]))] = {'Tag': row[12], 'Woche': row[13]}
                    line_count += 1
                elif csv_street == street and csv_house == house_number and csv_garbage == garbage_type:
                    result[(str(row[1]))] = {'Tag': row[12], 'Woche': row[13]}
                    break

    logging.info('Return: ' + str(result))

    return jsonify(result)
