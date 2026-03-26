import json

def parse_payload(req):
    try:
        # Step 1: Get data
        if req.is_json:
            data = req.get_json()
        else:
            data = json.loads(req.data.decode("utf-8"))

        # Step 2: Handle nested JSON string (VERY IMPORTANT)
        if isinstance(data, dict) and "raw" in data:
            try:
                # Try parsing inner JSON string
                inner = json.loads(data["raw"])
                data["raw"] = inner
            except Exception:
                pass  # keep as-is if not valid JSON

        return data

    except Exception as e:
        print("Error parsing:", str(e))
        return {
            "raw": req.data.decode("utf-8"),
            "error": str(e)
        }