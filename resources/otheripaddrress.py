from flask_restful import Resource, reqparse
# netaddr is a fast easy python library to make IP address related operations, but we can get rid of it and make it
# from scratch like: sum(bin(int(x)).count('1') for x in ,mask.split('.'))
from marshmallow import Schema, fields
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask import request, jsonify
import requests, logging, json
from logbase import call_logger, setup_logger
from database.country import country_data as cdata
from database.country import get_country_code


logger_visits = logging.getLogger("logger_visits")

class RemoteAddressSchema(Schema):
    ip = fields.String(required=True, default="0.0.0.0")
    country = fields.String(required=True, default="NA")
    languages = fields.List(fields.String(), required=False)
    currency = fields.String(required=False, default="NA")
    code = fields.String(required=False, default="NA")
    native = fields.String(required=False, default="NA")
    phone_code = fields.String(required=False, default="NA")
    continent = fields.String(required=False, default="NA")
    capital = fields.String(required=False, default="NA")
    



class RemoteAddress(MethodResource, Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, default='')

    
    @doc(description='Remomte address', tags=['IP Addreess'])
    @marshal_with(RemoteAddressSchema, code=200)  # marshalling
    #@use_kwargs({'species': fields.Str()})
    #@use_kwargs(RemoteAddressSchema, location=('json'))
    def get(self, ipaddr, mask=None):
        args = self.reqparse.parse_args()
        result = {}        
        result['ip'] = ipaddr
        country_code = get_country_code(ipaddr)
        country_data = cdata(country_code)
        result['country'] = country_data['Name']
        result['languages'] = country_data['Languages'].split(',')
        result['currency'] = country_data['Currency']
        result['phone_code'] = "+" + country_data['Phone']
        result['native'] = country_data['Native']
        result['continent'] = country_data['Continent']
        result['capital'] = country_data['Capital']
        result['code'] = country_code
        requester_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        requester_referrer = request.headers.get('User-Agent')
        logger_visits.info("{} request for Remote IP address: {}, Country: {}".format(requester_referrer,ipaddr, country_data['Name']))
        return result, 200
