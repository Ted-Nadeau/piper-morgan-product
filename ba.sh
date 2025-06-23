#!/bin/bash

# Check which version of app.py you're running
tail -5 web/app.py

# The last line should show:
# return HTMLResponse(content=html_content.replace("{api_base_url}", API_BASE_URL))
