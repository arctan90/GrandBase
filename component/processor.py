import secrets


def p_register(input_message):
    uuid = secrets.token_hex(16)
    # todo uuid存入db
    return base_ok(input_message, {'uuid': uuid})


def p_create_satellite(input_message):
    uuid = input_message['uuid']
    data = input_message['data']
    if data is None:
        return bad_req(input_message, 'request.data is missing')
    coordinate = data['coordinate']
    if coordinate is None:
        return bad_req(input_message, 'request.data.coordinate is missing')

    x = coordinate['x']
    y = coordinate['y']
    deg = coordinate['deg']

    # todo 创建卫星

    # todo sid 存入db
    sid = secrets.token_hex(16)
    return base_ok(input_message, {'sid': sid})


def p_forward(input_message):
    uuid = input_message['uuid']
    data = input_message['data']
    if data is None:
        return bad_req('request.data is missing')
    coordinate = data['coordinate']
    sid = data['sid']
    time_slot = data['timeSlot']
    unit = data['unit']

    coordinate = data['coordinate']
    return base_ok(input_message,
                   {'sid': sid, "type": "GCRS", "coordinate": {"x": 6400.00, "y": 6500.00, "deg": 163.14}})


def bad_req(input_message, e):
    return {'code': 403, 'requestId': input_message['requestId'], 'mid': input_message['mid'], 'message': e}


def internal_error(input_message, e):
    return {'code': 503, 'requestId': input_message['requestId'], 'mid': input_message['mid'], 'message': e}


def base_ok(input_message, data):
    return {'code': 200, 'requestId': input_message['requestId'], 'mid': input_message['mid'], 'data': data}
