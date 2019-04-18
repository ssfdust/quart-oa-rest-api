from flask_jwt_extended import JWTManager
from quart import jsonify, abort
from .helpers import is_token_revoked
from loguru import logger

jwt = JWTManager()


@jwt.unauthorized_loader
def unauthorized_callback(e):
    logger.error('未受权的访问')
    response = jsonify({
        "code": 401,
        "msg": "未授权的访问"
    })
    response.status_code = 401
    return response


@jwt.expired_token_loader
def token_expired():
    response = jsonify({
        "code": 401,
        "msg": "登录已过期"
    })
    logger.warning('登录过期')
    response.status_code = 401
    return response


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    from modules.users.models import User
    user = User.query.filter_by(username=identity).first()
    if user:
        return {
            'roles': [i.id for i in user.roles],
            'abilities': [i.id for i in user.abilities]
        }
    else:
        return {}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    check = is_token_revoked(decrypted_token)
    if check:
        return True
    else:
        return False


@jwt.user_loader_callback_loader
def get_user(identity):
    from modules.users.models import User
    if identity:
        user = User.query.filter_by(username=identity).first()
        return user
    else:
        print(identity)
        abort(401)


@jwt.user_loader_error_loader
def fail_load_user(identity):
    if identity['user'] is None:
        return jsonify({
            "code": 404,
            "msg": "用户名不存在"
        })
    else:
        return jsonify({
            "code": 404,
            "msg": "密码错误"
        })
