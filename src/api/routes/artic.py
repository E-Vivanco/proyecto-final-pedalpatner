from flask import Blueprint, request, jsonify, render_template
from api.models import db,Articulo,TallerArticulo
from flask_jwt_extended import JWTManager,get_jwt_identity,create_access_token,jwt_required
from werkzeug.security import generate_password_hash,check_password_hash

bpArticulo = Blueprint('bpArticulo', __name__)

@bpArticulo.route('/register_articulo', methods=['POST'])
#@jwt_required
def post_registarticulo():
    try:
        #id = get_jwt_identity()
        articulonom = request.json.get('articulonom')
        precio= request.json.get('precio')
        precio_oferta = request.json.get('precio_oferta')

        if not articulonom: return jsonify({"status": "failed", "code": 400, "msg": "articulo is required"}), 400
        if not precio: return jsonify({"status": "failed", "code": 400, "msg": "precio is required"}), 400
        if not precio_oferta: return jsonify({"status": "failed", "code": 400, "msg": "precio-oferta is required"}), 400

            #taller = Taller.query.filter(Taller.tallernom==tallernom).all()
        articulo = Articulo.query.filter_by(articulonom=articulonom).first()
        if articulo:
              return jsonify({"msg": "Articulo ya se encuentra registrado"}),400
    
        articulo = Articulo()
        articulo.articulonom = articulonom
        articulo.precio = precio
        articulo.precio_oferta = precio_oferta
        articulo.save()

        data ={
            "articulo": articulo.serialize_articulo()
        }
        return jsonify({"msg":"Exito al registrar Articulo", "articulo": data})
    except Exception as e:
        print("fala en articulo", e)

        return jsonify({"msg":"Ingreso de Articulo Fallido"})

@bpArticulo.route('/register_tallerarticulo', methods=['POST'])
#@jwt_required
def post_registrotallerarticulo():
    try:
        #id = get_jwt_identity()
        articulos_id = request.json.get('articulos_id')
        talleres_id = request.json.get('talleres_id')
        
        artictaller = TallerArticulo()
        artictaller.articulos_id = articulos_id
        artictaller.talleres_id = talleres_id

        artictaller.save()

        data ={
            "articulo-taller": artictaller.serialize_tallerarticulo()
        }
        return jsonify({"msg":"Exito con registro de taller-articulo","dato":data}),200
    except Exception as e:
        print("falla registro articulo taller",e)
    return jsonify({"msg":"Fallo al registrar tipo de articulo-taller"}),400