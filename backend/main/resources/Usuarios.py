from flask_restful import Resource
from flask import json, request, jsonify
from .. import db
from main.models import UsuarioModel
from main.auth.decorators import role_required

class Usuario(Resource):

    @role_required(roles=["admin"])
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_json()

    @role_required(roles=["admin"])
    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

    @role_required(roles=["admin"])
    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201

class Usuarios(Resource):

    @role_required(roles=["admin"])
    def get(self):
        page = 1
        per_page = 5
        usuarios = db.session.query(UsuarioModel)
        if request.get_json(silent=True):
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        usuarios = usuarios.paginate(page, per_page, True, 10)
        return jsonify({
            'usuarios': [usuario.to_json() for usuario in usuarios.items],
            'total': usuarios.total,
            'pages': usuarios.pages,
            'page': page
        })
    
    @role_required(roles=["admin"])
    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201