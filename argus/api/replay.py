
from flask import jsonify, g, request, url_for, json
from argus import db
from argus.models import Replay, ReplaySectorFever
from argus.api import bp

@bp.route('/api/replay', methods=['POST'])
def post_replay():
    post = request.get_json() or {}
    print(post)
    if 'date' not in post or 'summary' not in post or 'marketFever' not in post:
        # return bad_request('must include username, email and password fields')
        print('error')

    if 'sectorFevers' in post:
        fevers = post['sectorFevers']
        date = post['date']
        for fever in fevers:
            fever['date'] = date
            if 'sectorId' not in fever or 'fever' not in fever:
                continue
            new_sector_fever = ReplaySectorFever()
            new_sector_fever.from_dict(fever)
            db.session.add(new_sector_fever)

    # 大盘
    new_replay = Replay()
    new_replay.from_dict(post)
    db.session.add(new_replay)
    db.session.commit()
    response = jsonify(post)
    response.status_code = 201
    # response.headers['Location'] = url_for('api.post_replay', id=new_replay.id)
    return response

# 根据date获取replay详情

@bp.route('/api/replay', methods=['GET'])
def get_replay():
    params = request.args
    if 'date' not in params:
        print('error')

    date = request.args.get("date")
    
    resources = Replay.query.filter(
        Replay.date == date
    ).all()

    sectors = ReplaySectorFever.query.filter(
        ReplaySectorFever.date == date
    ).all()

    data = {
        'data': item.to_dict() for item in resources
    }
    # data['data'] = item.to_dict() for item in resources
    data['sector'] = [s.to_dict() for s in sectors]
    return data

@bp.route('/api/replays', methods=['GET'])
def get_replays():
    params = request.args
    if 'startDay' not in params or 'endDay' not in params:
        # 进行数据分页
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        data = Replay.to_collection_dict(Replay.query, page, per_page, 'api.get_replays')
        return jsonify(data)

    start_day = request.args.get("startDay") or ''
    end_day = request.args.get("endDay") or ''
    
    resources = Replay.query.filter(
        Replay.date >= start_day,
        Replay.date <= end_day
    ).all()
    data = {
        'data': [item.to_dict() for item in resources]
    }
    return data


@bp.route('/api/replay/fevers', methods=['GET'])
def get_replay_fevers():
    params = request.args
    if 'startDay' not in params or 'endDay' not in params:
        print('error')
    start_day = request.args.get("startDay") or ''
    end_day = request.args.get("endDay") or ''
    sector_ids = request.args.getlist("sectorIds[]") or []

    resources = ReplaySectorFever.query.filter(
        ReplaySectorFever.date >= start_day,
        ReplaySectorFever.date <= end_day,
        ReplaySectorFever.sectorId.in_(sector_ids)
    ).all()
    data = {
        'data': [item.to_dict() for item in resources]
    }
    return data
    
