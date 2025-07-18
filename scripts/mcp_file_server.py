#!/usr/bin/env python3
"""
Simple MCP Filesystem Server for Piper Morgan POC

This script provides a basic MCP server that exposes the uploads/ directory
as MCP resources. It's designed for POC testing without requiring Python 3.10+.

Note: This is a simulation server for the POC. In production, you would use
a proper MCP server implementation.
"""

import json
import os
import sys
import time
from pathlib import Path


class SimpleMCPFileServer:
    """Simple MCP filesystem server for POC testing"""

    def __init__(self, root_directory: str = "uploads"):
        self.root_directory = Path(root_directory)
        self.resources = []
        self._scan_directory()

    def _scan_directory(self):
        """Scan directory for files and create resource list"""
        if not self.root_directory.exists():
            return

        for file_path in self.root_directory.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                resource = {
                    "uri": f"file://{file_path.absolute()}",
                    "name": file_path.name,
                    "description": f"File from {self.root_directory}",
                    "mimeType": self._guess_mime_type(file_path.name),
                    "size": stat.st_size,
                    "lastModified": time.ctime(stat.st_mtime),
                }
                self.resources.append(resource)

    def _guess_mime_type(self, filename: str) -> str:
        """Guess MIME type from file extension"""
        ext = Path(filename).suffix.lower()
        mime_types = {
            ".pdf": "application/pdf",
            ".txt": "text/plain",
            ".md": "text/markdown",
            ".json": "application/json",
            ".csv": "text/csv",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        return mime_types.get(ext, "application/octet-stream")

    def handle_request(self, request: dict) -> dict:
        """Handle MCP request (simplified)"""
        method = request.get("method", "")

        if method == "resources/list":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {"resources": self.resources},
            }

        elif method == "resources/read":
            uri = request.get("params", {}).get("uri", "")
            return self._read_resource(uri, request.get("id"))

        elif method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"resources": {"subscribe": False, "listChanged": False}},
                    "serverInfo": {"name": "piper-morgan-file-server", "version": "1.0.0-poc"},
                },
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

    def _read_resource(self, uri: str, request_id) -> dict:
        """Read resource content"""
        if not uri.startswith("file://"):
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32602, "message": "Invalid URI format"},
            }

        file_path = Path(uri.replace("file://", ""))

        if not file_path.exists():
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": "File not found"},
            }

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": self._guess_mime_type(file_path.name),
                            "text": content,
                        }
                    ]
                },
            }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Failed to read file: {str(e)}"},
            }

    def run(self):
        """Run the MCP server using stdio transport"""
        try:
            for line in sys.stdin:
                try:
                    request = json.loads(line.strip())
                    response = self.handle_request(request)
                    print(json.dumps(response))
                    sys.stdout.flush()
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                    }
                    print(json.dumps(error_response))
                    sys.stdout.flush()

        except KeyboardInterrupt:
            pass


def main():
    """Main entry point"""
    # Change to script directory for relative paths
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)

    # Create server
    server = SimpleMCPFileServer()

    # Log startup to stderr (stdout is used for MCP protocol)
    print(
        f"MCP File Server started, serving {len(server.resources)} resources from uploads/",
        file=sys.stderr,
    )

    # Run server
    server.run()


if __name__ == "__main__":
    main()
