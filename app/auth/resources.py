from flask_restplus import Api,Resource,abort
from flask import request
from flask_jwt_extended import (create_access_token,create_refresh_token,
                                jwt_required,jwt_refresh_token_required,
                                get_jwt_identity,get_raw_jwt)
from .. import db
from models.model import User
from models.tokens import TokenBlacklist
from app.utils import UserDTO

api = UserDTO.api #namespace
model = UserDTO.userModel

@api.route('/signup')
class UserRegistration(Resource):
    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'})
    @api.expect(model,validate=True)
    def post(self):
        username=request.json.get('username')
        password=request.json.get('password')
        user = User.findByUsername(username)
        if user:
            return {'message': 'Existing user'}

        newUser = User(username=username,password = User.hash_password(password))
        try:
            newUser.save()
            access_token = create_access_token(identity=newUser.id)
            refresh_token = create_refresh_token(identity=newUser.id)
            return {
                'message': f'user {newUser.username} created',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except Exception as err:
            return {'message': err}


@api.route('/login')
class UserLogin(Resource):
    @api.doc(responses={200:'ok',400:'Client-side error',500:'Server-side error'})
    @api.expect(model,validate=True)
    def post(self):
        username=request.json.get('username')
        password=request.json.get('password')
        user = User.findByUsername(username)
        if not user:
            return {'message': f'user {username} does not exist'}

        if user.verify_password(password):
            # Access tokens are used to access protected routes
            # Refresh tokens are used to reissue tokens when they expire
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'message': f'user {user.username} logged in',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return {'message': 'Wrong password'}


@api.route('/logout/access')
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            token = TokenBlacklist(jti=jti)
            token.save()
            return {"message": "Access token has been removed"}
        except Exception as err:
            print(err)
            return {"message": "error"}


@api.route('/logout/refresh')
class userLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            token = TokenBlacklist(jti=jti)
            token.save()
            return {"message": "Refresh token has been removed"}
        except:
            return {"message": "error"}


# This functionality reissues access token with a refresh token after the 
# expiration of the access token
@api.route('/token/refresh')
class TokenRefresh(Resource):
    @jwt_refresh_token_required  # means can only be accessed using refresh tokens
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


@api.route('/allusers')
class AllUsers(Resource):
    def get(self):
        return User.getAllUsers()

    def delete(self):
        return User.dropAllUsers()


@api.route('/secret')
class SecretResource(Resource):
    @jwt_required
    def get(self):
        try:
            user = get_jwt_identity()
            jwt = get_raw_jwt()
            return {
                'answer': 42,
                'userId': user,
                'jwt': jwt
            }
        except Exception as err:
            return {"message":err}

