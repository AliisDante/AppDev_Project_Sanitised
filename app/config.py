from jwcrypto.jwk import JWK
from jwcrypto.common import base64url_encode

class Config:
    SECRET_KEY = "CENSORED"
    SQLALCHEMY_DATABASE_URI = "sqlite:///main.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_EXPIRY_TIME_IN_SECONDS = 60 * 60 * 24 * 14
    
    JWK = JWK(kid=1, kty="oct", alg="A128KW", enc="A128GCM", k=base64url_encode(SECRET_KEY[:16]))
    UPLOAD_FOLDER = '/static/productsDB'

    MAIL_SERVER = 'CENSORED'
    MAIL_PORT = 587
    MAIL_USERNAME = "CENSORED"
    MAIL_PASSWORD = f"CENSORED"
    MAIL_DEFAULT_SENDER = "CENSORED"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
