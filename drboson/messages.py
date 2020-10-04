def make_communication_message(run_id, project_id, message_type, payload):
    types = ['log', 'file', 'status']
    status_allowed_payload = ['pending', 'preparing', 'running', 'failed', 'completed']

    if message_type.lower() not in types:
        raise TypeError('drboson: Invalid message type')

    if message_type.lower() == 'status' and payload.lower() not in status_allowed_payload:
        raise ValueError('drboson: Invalid status')

    return {
        'run_id': run_id,
        'project_id': project_id,
        'type': message_type,
        'payload': payload
    }
