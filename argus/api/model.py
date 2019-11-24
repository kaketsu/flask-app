
from flask import jsonify, g, request, url_for, json
from argus import db
from argus.models import SelectModel
from argus.api import bp
from datetime import datetime

@bp.route('/api/model', methods=['POST'])
def post_model():
    post = request.get_json() or {}
    if 'modelName' not in post or 'modelDescription' not in post:
        # return bad_request('must include username,email and password fields')
        print('error')
    if 'id' in post:
        id = post['id']
        old_model = SelectModel.query.filter(SelectModel.id == id).first()
        print(old_model)
        old_model.modelName = post['modelName']
        old_model.modelDescription = post['modelDescription']
        old_model.updateTime = datetime.now()
        db.session.commit()
        response = jsonify(post)
        response.status_code = 201
        return response
    else:
        new_model = SelectModel()
        new_model.from_dict(post)
        db.session.add(new_model)
        db.session.commit()
        response = jsonify(post)
        response.status_code = 201
        return response

@bp.route('/api/models', methods=['GET'])
def get_models():
    params = request.args

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = SelectModel.to_collection_dict(SelectModel.query, page, per_page, 'api.get_replays')
    return jsonify(data)

@bp.route('/api/model/<int:id>', methods=['GET'])
def get_model(id):
    return jsonify(SelectModel.query.get_or_404(id).to_dict())
