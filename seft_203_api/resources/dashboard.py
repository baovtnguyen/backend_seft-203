from cerberus import Validator
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from seft_203_api.models.dashboard import DashboardModel
from seft_203_api.resources.helper import non_empty_string


def widget_validator(value):
    LOCATION_SCHEMA = {
        'title': {'required': True, 'type': 'string', 'minlength': 3},
        'widget_type': {'required': True, 'type': 'string', 'minlength': 3},
        'min_height': {'required': True, 'type': 'integer', 'min': 1},
        'min_width': {'required': True, 'type': 'integer', 'min': 1},
        'configs': {'required': True, 'type': 'dict'}
    }
    v = Validator(LOCATION_SCHEMA)
    if v.validate(value):
        return value
    else:
        raise ValueError(v.errors)


def _get_dashboard_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "title", type=non_empty_string, required=True
    )
    parser.add_argument(
        "layout_type", type=non_empty_string, required=True
    )
    parser.add_argument(
        "widgets", type=widget_validator, action="append", required=True
    )
    
    return parser


class Dashboard(Resource):

    @jwt_required()
    def put(self, dashboard_title):
        data = _get_dashboard_parser().parse_args(strict=True)

        dashboard = DashboardModel.find_one_by_title(title=dashboard_title, user_id=get_jwt_identity()) 
        if not dashboard:
            if dashboard_title != data['title']:
                return {"message": "Dashboard id must be match"}, 400
                
            new_dashboard = DashboardModel(**data, user_id=get_jwt_identity())
            new_dashboard.save_to_db()
            return {"message": f"Dashboard '{dashboard_title}' created successfully"}, 201

        if (dashboard_title != data['title'] and
        DashboardModel.find_one_by_title(title=data['title'], user_id=get_jwt_identity())):
            return {"message": f"Dashboard with title '{data['title']}' already exists"}, 400
        
        dashboard.title = data['title']
        dashboard.layout_type = data["layout_type"]
        dashboard.widgets = data['widgets']
        dashboard.update_to_db()
        return {"message": f"Dashboard '{dashboard_title}' updated successfully"}


class DashboardList(Resource):
    
    @jwt_required()
    def get(self):
        return {"dashboards": [x.json() for x in DashboardModel.find_all_by_user_id(user_id=get_jwt_identity())]}

