from flask_jwt_extended.utils import get_jwt_identity
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required

from seft_203_api.models.contact import ContactModel
from seft_203_api.models.user import UserModel

from seft_203_api.resources.helper import non_empty_string

def _get_parser():
    parser = reqparse.RequestParser()
    
    parser.add_argument(
        "first_name", type=non_empty_string, required=True
    )
    parser.add_argument(
        "last_name", type=non_empty_string, required=True
    )
    parser.add_argument(
        "title", type=non_empty_string, required=True
    )
    parser.add_argument(
        "department", type=non_empty_string, required=True
    )
    parser.add_argument(
        "project", type=non_empty_string, required=True
    )
    parser.add_argument(
        "avatar", type=non_empty_string, required=True
    )
  
    return parser

class Contact(Resource):

    @jwt_required()
    def get(self, contact_id):
        contact = ContactModel.find_one_by_id(contact_id, user_id=get_jwt_identity())
        if not contact:
            return {"message": f"Contact {contact_id} not found"}, 404
        return contact.json()


    @jwt_required()
    def put(self, contact_id):
        data = _get_parser().parse_args(strict=True)
        
        contact = ContactModel.find_one_by_id(contact_id, user_id=get_jwt_identity())
        if not contact:
            return {"message": f"Contact with id '{contact_id}' not found or not your own contact."}, 400

        if (contact.title != data['title'] and
        ContactModel.find_one_by_title(title=data['title'], user_id=get_jwt_identity())):
            return {"message": f"Contact with title '{data['title']}' already exists"}, 400
        
        contact.first_name = data['first_name']
        contact.last_name = data['last_name']
        contact.title = data['title']
        contact.department = data['department']
        contact.project = data['project']
        contact.avatar = data['avatar']
        contact.update_to_db()
        return contact.json()


    @jwt_required()
    def delete(self, contact_id):
        contact = ContactModel.find_one_by_id(contact_id, user_id=get_jwt_identity())
        if contact:
            contact.delete_from_db()
            return {"message": f"Contact {contact_id} deleted"}
        return {"message": f"Contact {contact_id} not found"}, 400


class ContactList(Resource):

    @jwt_required()
    def post(self):
        data = _get_parser().parse_args(strict=True)
        
        if ContactModel.find_one_by_title(data["title"]):
            return {
                "message": f"Contact with title '{data['title']}' already exists"
            }, 400  # bad request

        contact = ContactModel(**data, user_id=get_jwt_identity())
        contact.save_to_db()

        return {"message": f"Contact '{contact.title}' created successfully."}, 201  # Created


    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return {"contacts": [x.json() for x in ContactModel.find_all_by_user_id(user_id)]}

class ContactSearch(Resource):

    @jwt_required()
    def get(self):
        keyword = request.args['keyword']
        result = ContactModel.search_by_keyword(keyword, user_id=get_jwt_identity())
        return {"result": [contact.json() for contact in result]}