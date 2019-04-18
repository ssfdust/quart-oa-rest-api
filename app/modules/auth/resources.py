from . import blp
from quart.views import MethodView
from quart import current_app as app
from quart import jsonify


class LoginView(MethodView):
    async def get(self):
        app.logger.debug(1111)
        return jsonify({'code': 3})


login_view = LoginView.as_view('login')
blp.add_url_rule('/login', view_func=login_view)
