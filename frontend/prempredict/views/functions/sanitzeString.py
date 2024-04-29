import html
import re

def cleanString(input):
    input = re.sub(r'<script\b[^>]*>(.*?)</script>', '', input, flags=re.IGNORECASE)
    return html.escape(str(input).strip())