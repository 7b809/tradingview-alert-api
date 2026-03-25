import json

def parse_payload(req):
    try:
        print(req)
        if req.is_json:
            return req.get_json()
        else:
            return json.loads(req.data.decode("utf-8"))
    except Exception:
        return {"raw": req.data.decode("utf-8")}