from flask_restful import Resource, reqparse, abort
from api.todos.models import Todo
from api.todos.schemas import TodoSchema
from api.utils.decorators import use_schema
from flask_jwt import jwt_required, current_identity

todo_parser = reqparse.RequestParser()
todo_parser.add_argument(
    'text',
    type=str
)
todo_parser.add_argument(
    'completed',
    type=bool
)


class TodoListAPI(Resource):
    method_decorators = [jwt_required()]

    @use_schema(TodoSchema, many=True)
    def get(self):
        todos = current_identity.todos.all()
        return todos, 200

    @use_schema(TodoSchema, many=False)
    def post(self):
        args = todo_parser.parse_args()
        todo = Todo.create(text=args.text)
        current_identity.todos.append(todo)
        current_identity.save()
        return todo, 201


class TodoAPI(Resource):
    method_decorators = [jwt_required()]

    @use_schema(TodoSchema, many=False)
    def get(self, id):
        todo = current_identity.todos.filter_by(id=id).first()
        return todo, 200

    @use_schema(TodoSchema, many=False)
    def put(self, id):
        args = todo_parser.parse_args()
        todo = current_identity.todos.filter_by(id=id).first()
        todo.text = args.text
        return todo, 200

    def delete(self, id):
        todo = current_identity.todos.filter_by(id=id).first()
        todo.delete()
        return {}, 200
