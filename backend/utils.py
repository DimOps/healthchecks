def create_ui_obj(check, state):
    return {
        'id': check.id,
        'name': check.name,
        'host': check.host,
        'type': check.type,
        'state':
            {
                'ping_id': state.ping_id,
                'status': state.status,
                'lastDownStart': state.last_down_start,
                'lastDownEnd': state.last_down_end
            }
    }
