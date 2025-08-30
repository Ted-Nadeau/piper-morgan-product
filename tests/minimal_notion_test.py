# find_parent.py - Find accessible pages
import os

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
notion = Client(auth=os.environ["NOTION_API_KEY"])

# Search for accessible pages
results = notion.search(filter={"property": "object", "value": "page"}, page_size=10)

print("Accessible pages:")
for page in results["results"]:
    # Extract title safely
    title = "Untitled"
    if "properties" in page and "title" in page["properties"]:
        title_prop = page["properties"]["title"]
        if "title" in title_prop and len(title_prop["title"]) > 0:
            title = title_prop["title"][0]["text"]["content"]

    print(f"- {title}: {page['id']}")
