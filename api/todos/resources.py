from flask_restful import Resource, reqparse, abort
from api.todos.models import Todo
from api.todos.schemas import TodoSchema
from api.utils.decorators import use_schema

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
    @use_schema(TodoSchema, many=True)
    def get(self):
        return Todo.query.all(), 200

    @use_schema(TodoSchema, many=False)
    def post(self):
        args = todo_parser.parse_args()
        todo = Todo.create(text=args.text)
        return todo, 201


class TodoAPI(Resource):
    @use_schema(TodoSchema, many=False)
    def get(self, id):
        todo = Todo.query.get(id)
        return todo, 200
