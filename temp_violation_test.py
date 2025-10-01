from services.integrations.mcp.notion_adapter import NotionMCPAdapter
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter


class TestService:
    def __init__(self):
        self.calendar = GoogleCalendarMCPAdapter()
        self.notion = NotionMCPAdapter()
        self.slack = SlackSpatialAdapter()
