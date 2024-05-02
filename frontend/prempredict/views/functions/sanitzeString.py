import html
import re

def cleanString(input):
    try:
        input = re.sub(r'<script\b[^>]*>(.*?)</script>', '', input, flags=re.IGNORECASE)
    except:
        input = ""
    return html.escape(str(input).strip())