import functools
from flask_jwt_extended.utils import get_current_user, get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required

from seft_203_api.models.task import TaskModel
from seft_203_api.models.user import UserModel

from seft_203_api.resources.helper import non_empty_string

def _get_task_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "task", type=non_empty_string, required=True
    )
    parser.add_argument(
        "is_completed", type=bool, required=True, help="This field cannot be blank!"
    )
    return parser


class Task(Resource):
    
    @jwt_required()
    def get(self, task_id):
        
        task = TaskModel.find_one_by_id(task_id, user_id=get_jwt_identity())
        if not task:
            return {"message": f"Task with id '{task_id}' not found or not your own task"}, 404
        return task.json()

    
    @jwt_required()
    def put(self, task_id):

        data = _get_task_parser().parse_args(strict=True)

        task = TaskModel.find_one_by_id(task_id, user_id=get_jwt_identity())
        if not task:
            return {"message": f"Task with id '{task_id}' not found or not your own task"}, 404
            
        if (task.task != data['task'] and
        TaskModel.find_one_by_taskname(taskname=data['task'], user_id=get_jwt_identity())):
            return {"message": f"Task '{data['task']}' already exists"}, 400

        task.task = data['task']
        task.is_completed = data['is_completed']
        task.update_to_db()
        return task.json()


    @jwt_required()
    def delete(self, task_id):
        task = TaskModel.find_one_by_id(task_id, user_id=get_jwt_identity())
        if task:
            task.delete_from_db()
            return {"message": f"Task '{task.task}' deleted"}
            
        return {"message": f"Task not found"}, 400



class TaskList(Resource):

    @jwt_required()
    def post(self):
        data = _get_task_parser().parse_args(strict=True)

        if TaskModel.find_one_by_taskname(taskname=data['task'], user_id=get_jwt_identity()):
            return {"message": f"Task '{data['task']}' already exists"}, 400

        task = TaskModel(**data, user_id=get_jwt_identity())
        task.save_to_db()

        return {"message": f"Task '{task.task}' created successfully."}, 201  # Created
    

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return {"tasks": [x.json() for x in TaskModel.find_all_by_user_id(user_id)]}


class TaskSearch(Resource):

    @jwt_required()
    def get(self):
        keyword = request.args['keyword']
        result = TaskModel.search_by_keyword(keyword, user_id=get_jwt_identity())
        return {"result": [task.json() for task in result]}