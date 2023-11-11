import flask
from flask import jsonify, request, views

from errors import HttpError
from models import Session, Ads, User
from scheme import CreateAdv, UpdateAdv
from validate import validate

app = flask.Flask('api')

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response

@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


def get_adv(adv_id: int):
    advertisement = request.session.get(Ads, adv_id)
    if advertisement is None:
        raise HttpError(404, 'Advertisement not found')
    return advertisement


def add_adv(advertisement: Ads):
    request.session.add(advertisement)
    request.session.commit()

class AdsView(views.MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, adv_id: int):
        user = get_adv(adv_id)
        return jsonify(user.dict)

    def post(self):
        adv_data = validate(CreateAdv, request.json)
        user_id = adv_data['user_id']
        users = self.session.get(User, user_id)

        # Проверка на наличие пользователя в базе данных:
        if users is None:
            raise HttpError(
                400, f'user ID{user_id} not found'
            )

        advertisement = Ads(**adv_data)
        add_adv(advertisement)
        return jsonify({"id": advertisement.id})

    def patch(self, adv_id: int):
        advertisement = get_adv(adv_id)
        adv_data = validate(UpdateAdv, request.json)
        origin_id = advertisement.user_id

        for key, value in adv_data.items():
            # Проверка на изменение ID пользователя:
            if key == 'user_id':
                if value != origin_id:
                    raise HttpError(
                        400, 'field "user_id" cannot be changed'
                    )

            setattr(advertisement, key, value)
            add_adv(advertisement)
        return jsonify(advertisement.dict)

    def delete(self, adv_id: int):
        advertisement = get_adv(adv_id)
        self.session.delete(advertisement)
        self.session.commit()
        return jsonify({"status": "ok"})


adv_view = AdsView.as_view('adv_view')
app.add_url_rule(
    '/ads/<int:adv_id>', view_func=adv_view, methods=['GET', 'PATCH', 'DELETE']
)
app.add_url_rule('/ads', view_func=adv_view, methods=['POST'])


if __name__ == "__main__":
    app.run(debug=True)