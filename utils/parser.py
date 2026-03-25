import json

def parse_payload(req):
    try:
        print("Headers:", req.headers)
        print("Raw data:", req.data)

        if req.is_json:
            data = req.get_json()
        else:
            data = json.loads(req.data.decode("utf-8"))

        print("Parsed JSON:", data)
        return data
 
    except Exception as e:
        print("Error parsing:", str(e))
        return {"raw": req.data.decode("utf-8")}