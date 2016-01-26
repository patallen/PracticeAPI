from flask import request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource

from api.todos.schemas import TodoSchema
from api.utils.decorators import use_class_schema


class TodoListAPI(Resource):
    method_decorators = [jwt_required()]
    schema = TodoSchema()

    @use_class_schema(many=True)
    def get(self):
        todos = current_identity.todos.all()
        return todos, 200

    @use_class_schema(many=False)
    def post(self):
        todo = self.schema.load(request.get_json()).data
        current_identity.todos.append(todo)
        current_identity.save()
        return todo, 201


class TodoAPI(Resource):
    method_decorators = [jwt_required()]
    schema = TodoSchema()

    @use_class_schema(many=False)
    def get(self, id):
        todo = current_identity.todos.filter_by(id=id).first()
        return todo, 200

    @use_class_schema(many=False)
    def put(self, id):
        data = self.schema.load(request.get_json()).data
        todo = current_identity.todos.filter_by(id=id).first()
        todo.text = data.text
        return todo, 200

    def delete(self, id):
        todo = current_identity.todos.filter_by(id=id).first()
        todo.delete()
        return {}, 200
