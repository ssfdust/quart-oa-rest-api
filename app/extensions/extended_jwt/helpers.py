from datetime import datetime
from flask_jwt_extended import decode_token
from sqlalchemy.orm.exc import NoResultFound
from modules.users.models import TokenBlackList

def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)

def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']
    try:
        token = TokenBlackList.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True

def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.
    :param identity_claim:
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[identity_claim]
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = False
    try:
        blacked_token = TokenBlackList.query.filter_by(
            user_identity=user_identity,
            token_type=token_type
        ).one()
    except NoResultFound:
        TokenBlackList.create(
            jti=jti,
            token_type=token_type,
            user_identity=user_identity,
            expires=expires,
            revoked=revoked
        )
    else:
        blacked_token.update(
            jti=jti,
            expires=expires,
            token_type=token_type,
        )

def revoke_token(user):
    """
    Revokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    try:
        token = TokenBlackList.query.filter_by(user_identity=user).one()
        token.update(revoked=True)
    except NoResultFound:
        pass
