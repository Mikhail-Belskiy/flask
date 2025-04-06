from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Advert, Session

app = Flask('app')

class AdvertView(MethodView):

    def get(self, advert_id: int = None):
        with Session() as session:
            if advert_id is not None:
                advert = session.query(Advert).get(advert_id)
                if advert:
                    return jsonify(advert.dict), 200
                else:
                    return jsonify({'error': 'Advert not found'}), 404
            else:
                adverts = session.query(Advert).all()
                return jsonify([advert.dict for advert in adverts]), 200

    def post(self):
        json_data = request.json
        with Session() as session:
            advert = Advert(
                title=json_data['title'],
                description=json_data['description'],
                owner_id=json_data['owner_id']
            )
            session.add(advert)
            session.commit()
            return jsonify(advert.dict), 201

    def patch(self, advert_id: int):
        with Session() as session:
            advert = session.query(Advert).get(advert_id)
            json_data = request.json
            if advert:
                if 'title' in json_data:
                    advert.title = json_data['title']
                if 'description' in json_data:
                    advert.description = json_data['description']
                if 'owner_id' in json_data:
                    advert.owner_id = json_data['owner_id']
                session.commit()
                return jsonify(advert.dict), 200
            else:
                return jsonify({'error': 'Advert not found'}), 404

    def delete(self, advert_id: int):
        with Session() as session:
            advert = session.query(Advert).get(advert_id)
            if advert:
                session.delete(advert)
                session.commit()
                return jsonify({'message': 'Advert deleted successfully'}), 204
            else:
                return jsonify({'error': 'Advert not found'}), 404

# Роуты API
advert_view = AdvertView.as_view('advert_view')
app.add_url_rule('/api/v1/adverts', view_func=advert_view, methods=['POST', 'GET'])
app.add_url_rule('/api/v1/adverts/<int:advert_id>', view_func=advert_view, methods=['GET', 'PATCH', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)