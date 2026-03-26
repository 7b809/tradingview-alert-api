import json
import re

def parse_payload(req):
    raw_data = req.data.decode("utf-8")

    try:
        # 🔥 Fix ONLY multiline text field safely
        def fix_text(match):
            content = match.group(1)
            fixed = content.replace("\n", "\\n")
            return f'"text":"{fixed}"'

        cleaned = re.sub(r'"text":"(.*?)"', fix_text, raw_data, flags=re.DOTALL)

        data = json.loads(cleaned)

        return data

    except Exception as e:
        print("Error parsing:", str(e))
        return {
            "raw": raw_data,
            "error": str(e)
        }