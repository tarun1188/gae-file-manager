__author__ = 'Tarun'
import logging
from base import BaseHandler
from models.models import User
from services.helper import Helper
import json
import hashlib

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class LoginHandler(BaseHandler):

    def __init__(self, request, response):
        super(LoginHandler, self).__init__(request, response)

    def create_user(self):
        params = json.loads(self.request.body)
        user_id = params.get("user_id").lower()
        password = params.get("password").lower()
        response_dict = dict()
        params_satisfied = Helper.params_satisfied(params, ["user_id", "password"])

        if not params_satisfied.get("is_satisfied"):
            self.response.status = 400
            response_dict.update(msg=params_satisfied.get("msg"))
        else:
            user_exists = Helper.fetch_entity(User, user_id=user_id, is_deleted=False)
            if not user_exists:
                user = User()
                md5_generator = hashlib.md5()
                md5_generator.update(password)
                user.user_id = user_id
                user.password = md5_generator.hexdigest()
                user.put()
                response_dict.update(msg="User created successfully")
            else:
                response_dict.update(msg="User already exists")

        self.render_json(response_dict)