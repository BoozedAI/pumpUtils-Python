import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

try:
    from pumpCtrl import ccontrol as control
except Exception as e:
    control = None
    _import_error = e


AUTH_TOKEN = None  # set via serve(auth_token="...")


class PumpRequestHandler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Auth-Token")

    def _send(self, code=200, payload=None):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        if payload is not None:
            self.wfile.write(json.dumps(payload).encode("utf-8"))

    def _authorized(self):
        if AUTH_TOKEN is None:
            return True
        token = self.headers.get("X-Auth-Token") or self.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        return token == AUTH_TOKEN

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            status = {
                "ok": True,
                "controller": control is not None,
            }
            if control is None:
                status["error"] = str(_import_error)
            return self._send(200, status)

        if parsed.path == "/stop":
            if control is None:
                return self._send(500, {"error": str(_import_error)})
            if not self._authorized():
                return self._send(401, {"error": "unauthorized"})
            qs = parse_qs(parsed.query)
            try:
                pnum = int(qs.get("p", [None])[0])
            except Exception:
                return self._send(400, {"error": "missing or invalid 'p' (pump index)"})
            try:
                control.stopPump(pnum)
            except Exception as e:
                return self._send(500, {"error": str(e)})
            return self._send(200, {"stopped": pnum})

        if parsed.path == "/run":
            if control is None:
                return self._send(500, {"error": str(_import_error)})
            if not self._authorized():
                return self._send(401, {"error": "unauthorized"})
            qs = parse_qs(parsed.query)
            try:
                pnum = int(qs.get("p", [None])[0])
                volume = float(qs.get("v", [None])[0])
            except Exception:
                return self._send(400, {"error": "missing or invalid 'p' (pump index) or 'v' (ml)"})

            # run in background so request returns immediately
            def _run():
                try:
                    control.runPump(pnum, volume)
                except Exception:
                    pass

            t = threading.Thread(target=_run, daemon=True)
            t.start()
            return self._send(200, {"started": pnum, "volume": volume})

        return self._send(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path not in ("/run", "/stop"):
            return self._send(404, {"error": "not found"})
        if control is None:
            return self._send(500, {"error": str(_import_error)})
        if not self._authorized():
            return self._send(401, {"error": "unauthorized"})

        length = int(self.headers.get("Content-Length", 0))
        try:
            body = self.rfile.read(length) if length else b"{}"
            data = json.loads(body.decode("utf-8"))
        except Exception:
            return self._send(400, {"error": "invalid JSON"})

        if parsed.path == "/stop":
            try:
                pnum = int(data.get("p"))
            except Exception:
                return self._send(400, {"error": "missing or invalid 'p' (pump index)"})
            try:
                control.stopPump(pnum)
            except Exception as e:
                return self._send(500, {"error": str(e)})
            return self._send(200, {"stopped": pnum})

        if parsed.path == "/run":
            try:
                pnum = int(data.get("p"))
                volume = float(data.get("v"))
            except Exception:
                return self._send(400, {"error": "missing or invalid 'p' (pump index) or 'v' (ml)"})

            def _run():
                try:
                    control.runPump(pnum, volume)
                except Exception:
                    pass

            t = threading.Thread(target=_run, daemon=True)
            t.start()
            return self._send(200, {"started": pnum, "volume": volume})


def serve(host="0.0.0.0", port=8080, auth_token=None):
    global AUTH_TOKEN
    AUTH_TOKEN = auth_token
    httpd = HTTPServer((host, port), PumpRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    serve()
