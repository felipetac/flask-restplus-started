from flask import current_app
import jwt
from app.mod_user.service import Service as UserService
from app.mod_auth.form import LoginForm

class Service:

    @staticmethod
    def get_key(json_obj):
        form = LoginForm.from_json(json_obj)
        if form.validate_on_submit():
            user = UserService.get_by_email(form.email.data, serializer=False)
            if user and user.password == form.password.data:
                payloads = {"user": user.name, "email": user.email}
                encoded_jwt = jwt.encode(payloads, current_app.config["SECRET_KEY"],
                                         current_app.config["JWT_ALGORITHM"])
                return {"data": {"key": encoded_jwt.decode("utf-8")}}
            return {"form": "Usuário ou senha inválidos!"}
        return {"form": form.errors}
