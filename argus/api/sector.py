from flask import jsonify, g, request, url_for
from argus import db
from argus.models import Sector
from argus.api import bp

@bp.route('/api/sectors', methods=['GET'])
def get_sectors():
    no_page = request.args.get("nopage") or False
    search = request.args.get("search") or ''
    if no_page:
        resources = Sector.query.filter(Sector.sectorName.contains(search)).all()
        data = {
            'data': [item.to_dict() for item in resources]
        }
        return data

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Sector.to_collection_dict(Sector.query, page, per_page, 'api.get_sectors')
    return jsonify(data)

    # post = request.get_json() or {}
    # print(post)

    # if 'sectorName' not in post:
    #     print('error')
   
    # new_sector = Sector()
    # new_sector.from_dict(post)
    # db.session.add(new_sector)
    # db.session.commit()
    # response = jsonify(post)
    # response.status_code = 201
    # return response


@bp.route('/api/sector/<int:id>', methods=['GET'])
def get_sector(id):
    return jsonify(Sector.query.get_or_404(id).to_dict())

@bp.route('/api/sector', methods=['POST'])
def post_sector():
    post = request.get_json() or {}
    print(post)

    if 'sectorName' not in post:
        # return bad_request('must include username, email and password fields')
        print('error')
   
    new_sector = Sector()
    new_sector.from_dict(post)
    db.session.add(new_sector)
    db.session.commit()
    response = jsonify(post)
    response.status_code = 201
    return response