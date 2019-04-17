from database import (
    db,
    SurrogatePK,
    Model
)
from sqlalchemy import UniqueConstraint

class TokenBlackList(SurrogatePK, Model):
    """
    Token Black List Table
    """
    __tablename__ = "tokens_in_use"

    user_identity = db.Column(db.String(50), nullable=False)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("token_type", "user_identity", name='token_in_use_unique'),
    )

    def __init__(self, jti, token_type, **kwargs):
        db.Model.__init__(self, jti=jti,
                          token_type=token_type, **kwargs)

    def __repr__(self):  # pragma: nocover
        return '<TokenInUse({name!r})>'.format(name=self.user_identity)
