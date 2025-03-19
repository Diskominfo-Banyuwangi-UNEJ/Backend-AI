class UserController:
    def __init__(self):
        self.model = User

    def get_all(self):
        return self.model.query.all()

    def get_by_id(self, id):
        return self.model.query.get(id)

    def create(self, data):
        user = self.model(**data)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, id, data):
        user = self.get_by_id(id)
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    def delete(self, id):
        user = self.get_by_id(id)
        db.session.delete(user)
        db.session.commit()
        return user
