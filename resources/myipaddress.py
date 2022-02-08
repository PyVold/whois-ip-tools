from flask_restful import Resource
from marshmallow import Schema, fields
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask import request, jsonify, Response
import requests, logging, json
from logbase import call_logger, setup_logger
from database.country import country_data as cdata
from database.country import get_country_code


logger_visits = logging.getLogger("logger_visits")

class MyIpAddressSchema(Schema):
    ip = fields.String(required=True)
    country = fields.String(required=True, default="NA")
    languages = fields.List(fields.String(), required=False)
    currency = fields.String(required=False, default="NA")
    code = fields.String(required=False, default="NA")
    native = fields.String(required=False, default="NA")
    phone_code = fields.String(required=False, default="NA")
    continent = fields.String(required=False, default="NA")
    capital = fields.String(required=False, default="NA")


class MYIP(MethodResource, Resource):
    @doc(description='My IP address', tags=['IP Addreess'])
    @marshal_with(MyIpAddressSchema, code=200)  # marshalling
    def get(self):
        result = {}
        ipaddr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        #all_info = geolocation(ipaddr)
        result['ip'] = ipaddr
        country_code = get_country_code(ipaddr)
        country_data = cdata(country_code)
        result['languages'] = country_data['Languages'].split(',')
        result['currency'] = country_data['Currency']
        result['country'] = country_data['Name']
        result['phone_code'] = "+" + country_data['Phone']
        result['native'] = country_data['Native']
        result['continent'] = country_data['Continent']
        result['capital'] = country_data['Capital']
        result['code'] = country_code
        logger_visits.info("IP address: {}, Country: {}".format(ipaddr, country_data['Name']))
        return result

def geolocation(ipaddr):
    url = "https://geolocation-db.com/json/{}&position=true".format(ipaddr)
    geoloc = requests.get(url).json()
    return geoloc
