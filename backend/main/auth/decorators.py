from .. import jwt
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def role_required(roles):
    def decorator(function):
        def wrapper(*args, **kwargs):
            # Verificar que el token sea valido
            verify_jwt_in_request()
            # Obtener los claims del token
            claims = get_jwt()

            # Verificar si el rol del usuario esta en la lista de roles permitidos
            if claims["sub"]["role"] in roles:
                return function(*args, **kwargs)
            else:
                return "Unauthorized", 403
        return wrapper
    return decorator

@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return {
        "usuarioId": usuario.id,
        "role": usuario.role
    }

@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        "id": usuario.id,
        "role": usuario.role,
        "email": usuario.email
    }
    