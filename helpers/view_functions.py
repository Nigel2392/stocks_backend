import json


def parse_request_body(request):
    raw_data = request.body
    """https://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django"""
    body_unicode = raw_data.decode('utf-8')
    body = json.loads(body_unicode)
    return body
