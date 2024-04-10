from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoCompraModel

class ProductoCompra(Resource):
    
    def get(self, id):
        productoCompra = db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            return productoCompra.to_json()
        except:
            return "Resosurce not found", 404
        
    def put(self, id):
        productoCompra = db.session.query(ProductoCompraModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(productoCompra, key, value)
        try:
            db.session.add(productoCompra)
            db.session.commit()
            return productoCompra.to_json(), 201
        except:
            return "An error ocurred", 400
        
    def delete(self, id):
        productoCompra = db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            db.session.delete(productoCompra)
            db.session.commit()
            return "", 204
        except:
            return "An error ocurred", 400

class ProductosCompras(Resource):
    
    def get(self):
        page = 1
        per_page = 5
        productosCompras = db.session.query(ProductoCompraModel)
        if request.get_json(silent=True):
            filters = request.get_json().items()
            for key, value in filters:
                if key == "page":
                    page = int(value)
                elif key == "per_page":
                    per_page = int(value)
        productosCompras = productosCompras.paginate(page, per_page, True, 10)
        return jsonify({"productosCompras": [productoCompra.to_json() for productoCompra in productosCompras.items],
                        "total": productosCompras.total,
                        "pages": productosCompras.pages,
                        "page": page})
    
    def post(self):
        productoCompra = ProductoCompraModel.from_json(request.get_json())
        db.session.add(productoCompra)
        db.session.commit()
        return productoCompra.to_json(), 201
    
