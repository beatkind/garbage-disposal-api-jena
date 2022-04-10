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

# home
@app.route('/', methods=['GET'])
def home():
    return '<h1> GDAJ - garbage disposal api jena</h1>'

# get by street
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
                    result[(str(csv_garbage))] = {
                        'Tag': convertday(row[12]), 'Woche': convertweek(row[13])}
                    line_count += 1
                elif csv_street == street and csv_house == house_number and csv_garbage == garbage_type:
                    result[(str(csv_garbage))] = {
                        'Tag': convertday(row[12]), 'Woche': convertweek(row[13])}
                    break

    logging.info('Return: ' + str(result))

    return jsonify(result)

# get streets
@app.route('/streets', methods=['GET'])
def all_streets():

    result = []

    logging.info('Request - ' + str(request.user_agent))

    with open('entsorgungstermine.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                result.append(str(row[2]))

    result = list(dict.fromkeys(result))

    logging.info('Return: ' + str(result))

    return jsonify(result)

# get house numbers
@app.route('/houses', methods=['GET'])
def houses_of_street():
    if 'street' in request.args:
        street = str(request.args['street']).lower()
    else:
        abort(400, 'Street is missing')

    result = []

    logging.info('Request - ' + str(request.user_agent) + ': ' + street)

    with open('entsorgungstermine.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                csv_street = row[2].lower()

                if street == csv_street:
                    result.append(str(row[3]))

    if not result:
        abort(404, 'Street not found')
    else:
        result = list(dict.fromkeys(result))

    logging.info('Return: ' + str(result))

    return jsonify(result)

##################
# Helper         #
##################

# convert day
def convertday(tinyday):

    if tinyday == 'Mo':
        result = 'Montag'
    elif tinyday == 'Di':
        result = 'Dienstag'
    elif tinyday == 'Mi':
        result = 'Mittwoch'
    elif tinyday == 'Do':
        result = 'Donnerstag'
    elif tinyday == 'Fr':
        result = 'Freitag'
    elif tinyday == 'Sa':
        result = 'Samstag'
    elif tinyday == 'So':
        result = 'Sontag'

    return str(result)

# convert week
def convertweek(tinyweek):

    if tinyweek == 'g':
        result = 'gerade'
    elif tinyweek == 'u':
        result = 'ungerade'
    elif tinyweek == 'w':
        result = 'wöchentlich'

    return str(result)

##################
# error handling #
##################


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(403)
def resource_access_forbiden(e):
    return jsonify(error=str(e)), 403


@app.errorhandler(400)
def resource_bad_request(e):
    return jsonify(error=str(e)), 400
