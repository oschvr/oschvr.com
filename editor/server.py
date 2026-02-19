#!/usr/bin/env python3
"""Local server for Hugo blog post editor with S3 image upload."""

import json
import os
import re
import subprocess
import tempfile
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080
S3_BUCKET = "oschvr"
S3_REGION = "us-west-2"


class EditorHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        if self.path == "/upload":
            self._handle_upload()
        else:
            self.send_error(404)

    def _handle_upload(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._json_response(400, {"error": "Expected multipart/form-data"})
            return

        # Parse boundary from Content-Type
        m = re.search(r"boundary=(.+)", content_type)
        if not m:
            self._json_response(400, {"error": "No boundary in Content-Type"})
            return
        boundary = m.group(1).strip()

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        # Parse multipart manually
        file_data, original_name = self._parse_multipart(body, boundary)
        if file_data is None:
            self._json_response(400, {"error": "No file provided"})
            return

        name, ext = os.path.splitext(original_name)
        # Clean name: remove spaces and illegal characters
        clean_name = re.sub(r"[^a-zA-Z0-9_\-]", "", name.replace(" ", "_"))
        if not clean_name:
            clean_name = "image"
        # Format: YYYY/MM/DD_NAME.EXT
        now = time.localtime()
        s3_key = f"{now.tm_year}/{now.tm_mon:02d}/{now.tm_mday:02d}/{clean_name}{ext}"

        # Write to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        try:
            tmp.write(file_data)
            tmp.close()

            # Upload via AWS CLI
            s3_path = f"s3://{S3_BUCKET}/{s3_key}"
            result = subprocess.run(
                [
                    "aws", "s3", "cp", tmp.name, s3_path,
                    "--acl", "public-read",
                    "--region", S3_REGION,
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                self._json_response(500, {"error": result.stderr.strip()})
                return

            url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{s3_key}"
            self._json_response(200, {"url": url, "filename": original_name})
        finally:
            os.unlink(tmp.name)

    def _parse_multipart(self, body, boundary):
        """Parse multipart form data, return (file_bytes, filename) or (None, None)."""
        boundary_bytes = boundary.encode()
        # Parts are separated by --boundary
        parts = body.split(b"--" + boundary_bytes)
        for part in parts:
            # Skip preamble/epilogue
            if part in (b"", b"--\r\n", b"--"):
                continue
            part = part.strip(b"\r\n")
            if part == b"--":
                continue
            # Split headers from body at double CRLF
            sep = part.find(b"\r\n\r\n")
            if sep == -1:
                continue
            headers_raw = part[:sep].decode("utf-8", errors="replace")
            file_body = part[sep + 4:]
            # Strip trailing \r\n before next boundary
            if file_body.endswith(b"\r\n"):
                file_body = file_body[:-2]

            # Check if this part has a filename
            fn_match = re.search(r'filename="([^"]+)"', headers_raw)
            if fn_match:
                return file_body, os.path.basename(fn_match.group(1))
        return None, None

    def _json_response(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(("127.0.0.1", PORT), EditorHandler)
    print(f"Editor running at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
