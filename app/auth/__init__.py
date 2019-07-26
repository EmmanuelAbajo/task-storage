from flask import Blueprint
from flask_restplus import Api

auth = Blueprint('auth',__name__)

api = Api(app=auth,doc='/docs',
            title='User manager',
            description='A User management system')

from . import resources

api.add_namespace(resources.api,path='/users')