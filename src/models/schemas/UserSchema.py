from config import ma, db
from models.UserModel import User
from marshmallow_sqlalchemy import fields 

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

user_schema = UserSchema()