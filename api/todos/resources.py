from flask import request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource

from api.todos.schemas import TodoSchema, TodoListSchema
from api.todos.models import TodoList
from api.utils.decorators import use_class_schema


class ListsAPI(Resource):
    method_decorators = [jwt_required()]
    schema = TodoListSchema()

    @use_class_schema(many=True)
    def get(self):
        """
        Return All TodoLists for User
        => GET /lists
        """
        todo_lists = current_identity.todo_lists.all()
        return todo_lists, 200

    @use_class_schema(many=False)
    def post(self):
        """
        Add a new TodoList for User
        => POST /lists
        """
        todo_list = self.schema.load(request.get_json()).data
        current_identity.todo_lists.append(todo_list)
        current_identity.save()
        return todo_list, 200


class ListAPI(Resource):
    method_decorators = [jwt_required()]
    schema = TodoListSchema()

    @use_class_schema(many=False)
    def get(self, id):
        """
        Return info on a single TodoList (not the todos within)
        => GET /lists/<id>
        """
        todo_list = TodoList.query.get(id)
        return todo_list, 400

    @use_class_schema(many=False)
    def patch(self, id):
        """
        Edit the information of a single TodoList (not the todos)
        => PATCH /lists/<id>
        """
        data = self.schema.load(request.get_json().data)
        todo_list = TodoList.query.get(id)
        todo_list.title = data.title
        todo_list.save()
        return todo_list, 400

    @use_class_schema(many=False)
    def delete(self, id):
        """
        Delete a TodoList and all of it's underlying todos.
        => DELETE /lists/<id>
        """
        todo_list = TodoList.query.get(id)
        if todo_list in current_identity.todo_lists:
            todo_list.delete()
            return {}, 204
        else:
            return {}, 404


class TodoListAPI(Resource):
    method_decorators = [jwt_required()]
    schema = TodoSchema()

    @use_class_schema(many=True)
    def get(self, id):
        """
        Retrieve all Todos for a specific TodoList
        => GET /lists/<id>/todos
        """
        todo_list = TodoList.query.get(id)
        if todo_list and todo_list.user is current_identity:
            return todo_list.todos.all(), 200
        else:
            return {}, 404

    @use_class_schema(many=False)
    def post(self):
        """
        Create a Todo for a specific TodoList
        => POST /lists/<id>/todos
        """
        todo_list = TodoList.query.get(id)
        if todo_list in current_identity.todo_lists:
            todo = self.schema.load(request.get_json()).data
            todo_list.todos.append(todo)
            current_identity.save()
            return todo, 201
        else:
            return {}, 404


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

    @use_class_schema(many=False)
    def patch(self, id):
        data = self.schema.load(request.get_json()).data
        todo = current_identity.todos.filter_by(id=id).first()
        for key, val in data.to_dict().iteritems():
            setattr(todo, key, val)
        todo.save()
        return todo, 200

    def delete(self, id):
        todo = current_identity.todos.filter_by(id=id).first()
        todo.delete()
        return {}, 204
