from flask import Blueprint,make_response
from flask_restplus import Api
import json
from app.utils import myConverter


bp = Blueprint('bp',__name__)
api = Api(app=bp,doc='/docs',
            title='Todos manager',
            description='A Todo management system')

# This allows datetime objects to be json serializable
@api.representation('application/json')
def output_json(data,code,headers=None):
    resp = make_response(json.dumps(data,default=myConverter),code)
    resp.headers.extend(headers or {})
    return resp


from . import resources

api.add_namespace(resources.api,path='/todos')
