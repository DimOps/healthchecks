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
                'lastDownStart': state.lastdownstart,
                'lastDownEnd': state.lastdownend
            }
    }


def outage_in_percentage(report):
    all = report['unknown'] + report['up'] + report['down']
    out = {'unknown': 0, 'up': 0, 'down': 0}
    out['unknown'] = round((report['unknown']/all)*100, 2)
    out['up'] = round((report['up']/all)*100, 2)
    out['down'] = round((report['down']/all)*100)

    return out
