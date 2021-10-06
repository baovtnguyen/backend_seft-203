from datetime import datetime
from datetime import timezone
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jti 
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from seft_203_api.models.user import UserModel
from seft_203_api.models.tokenblocklist import TokenBlocklist

from flask import current_app as app
from seft_203_api.extensions import bcrypt
from seft_203_api.extensions import jwt
from seft_203_api.db import db

from seft_203_api.resources.helper import non_empty_string

def _get_user_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=non_empty_string, required=True
    )
    parser.add_argument(
        "password", type=non_empty_string, required=True
    )
    return parser


class UserRegister(Resource):

    @classmethod
    def _validate_data(cls):
        parser_copy = _get_user_parser().copy()
        parser_copy = parser_copy.add_argument(
            "full_name", type=non_empty_string, required=True
        )
        
        data = parser_copy.parse_args(strict=True)
        return data

    def post(self):
        data = UserRegister._validate_data()

        if UserModel.find_by_username(data["username"]):
            return {
                "message": "A user with that username already exists"
            }, 400  # bad request

        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8', 'ignore')
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201  # Created


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted."}, 200


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader  
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

def _create_tokens(identity):
    refresh_token = create_refresh_token(identity=identity)
    refresh_jti = get_jti(refresh_token)
    access_token = create_access_token(identity=identity, fresh=True, additional_claims={"refresh_jti": refresh_jti})

    return {"access_token": access_token, "refresh_token": refresh_token}


class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        data = _get_user_parser().parse_args(strict=True)
        user = UserModel.find_by_username(data["username"])
        if user and bcrypt.check_password_hash(user.password, data['password']):
            tokens = _create_tokens(user.id)
            return tokens, 200

        return {"message": "Invalid credentials"}, 401


class UserLogout(Resource):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        refresh_jti = get_jwt()["refresh_jti"]
        db.session.add(TokenBlocklist(jti=refresh_jti, created_at=now))
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return {"message": "JWT revoked"}, 200


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False, additional_claims={"refresh_jti": get_jwt()["jti"]})
        return {"access_token": new_token}, 200


