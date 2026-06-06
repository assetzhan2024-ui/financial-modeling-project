"""
server/app.py
=============
HTTP-сервер: маршрутизация запросов и отдача статических файлов.

Этот модуль знает только о транспорте (HTTP) и роутинге.
Вся бизнес-логика делегирована server/handlers.py.
<<<<<<< HEAD
"""

import json
import math
import os
from datetime import datetime
=======

Поддерживает структуру папок проекта:

    automatic/
      templates/index.html      → отдаётся по GET /
      styles/style.css          → отдаётся по GET /styles/style.css
      script/app.js             → отдаётся по GET /script/app.js

index.html ссылается на «../styles/style.css» и «../script/app.js» —
браузер разворачивает их в /styles/style.css и /script/app.js.
Сервер маппит эти URL-префиксы на реальные папки на диске.
"""

import json
import os
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from server.handlers import (
    handle_status,
    handle_chart,
    handle_fundamentals,
    handle_tickers,
    handle_fetch_post,
    handle_stop_post,
    handle_kase_test,
    handle_clear_post,
    handle_export,
<<<<<<< HEAD
    handle_export_dcf,
=======
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
)

MIME_TYPES: dict[str, str] = {
    ".html": "text/html; charset=utf-8",
    ".css":  "text/css; charset=utf-8",
    ".js":   "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png":  "image/png",
    ".ico":  "image/x-icon",
    ".svg":  "image/svg+xml",
}

<<<<<<< HEAD
_project_root: str = ""

=======
# Корень проекта (устанавливается из main через configure())
# Ожидаемая структура:
#   <project_root>/templates/index.html
#   <project_root>/styles/style.css
#   <project_root>/script/app.js
_project_root: str = ""

# Таблица маппинга: URL-префикс → подпапка в проекте
# Порядок важен: более длинные префиксы должны идти первыми.
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
_URL_TO_DIR: list[tuple[str, str]] = [
    ("/styles/",    "styles"),
    ("/script/",    "script"),
    ("/templates/", "templates"),
]

<<<<<<< HEAD
=======
# URL корня → файл внутри templates/
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
_ROOT_INDEX = "templates/index.html"


def configure(project_root: str) -> None:
<<<<<<< HEAD
=======
    """
    Установить корневую директорию проекта.

    Ожидается структура:
        project_root/
          templates/index.html
          styles/style.css
          script/app.js
    """
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
    global _project_root
    _project_root = project_root


def _resolve_file(url_path: str) -> str | None:
<<<<<<< HEAD
    """Разрешить URL-путь в абсолютный путь к файлу на диске."""
    url_path = url_path.split("?")[0].split("#")[0]

    if url_path in ("/", ""):
        candidate = os.path.join(_project_root, _ROOT_INDEX)
        return candidate if os.path.isfile(candidate) else None

=======
    """
    Разрешить URL-путь в абсолютный путь к файлу на диске.
    Возвращает None если файл не найден или путь небезопасен.
    """
    # Нормализуем URL: убираем query string и fragment
    url_path = url_path.split("?")[0].split("#")[0]

    # Корневой путь → index.html
    if url_path in ("/", ""):
        candidate = os.path.join(_project_root, _ROOT_INDEX)
        print(f"  [resolve] / → {candidate} exists={os.path.isfile(candidate)}")
        return candidate if os.path.isfile(candidate) else None

    # Перебираем маппинги URL-префиксов
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
    for url_prefix, dir_name in _URL_TO_DIR:
        if url_path.startswith(url_prefix):
            filename = url_path[len(url_prefix):].replace("..", "").lstrip("/")
            if not filename:
                return None
            candidate = os.path.join(_project_root, dir_name, filename)
<<<<<<< HEAD
            return candidate if os.path.isfile(candidate) else None

    safe = url_path.lstrip("/").replace("..", "")
    candidate = os.path.join(_project_root, safe)
=======
            print(f"  [resolve] {url_path} → {candidate} exists={os.path.isfile(candidate)}")
            return candidate if os.path.isfile(candidate) else None

    # Fallback: плоская раскладка — файл прямо в корне
    safe = url_path.lstrip("/").replace("..", "")
    candidate = os.path.join(_project_root, safe)
    print(f"  [resolve fallback] {url_path} → {candidate} exists={os.path.isfile(candidate)}")
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
    return candidate if os.path.isfile(candidate) else None


# ── Маршрутные таблицы ────────────────────────────────────────────────────────
_GET_ROUTES: dict = {
    "/api/status":       lambda qs: handle_status(qs),
    "/api/chart":        lambda qs: handle_chart(qs),
    "/api/fundamentals": lambda qs: handle_fundamentals(qs),
    "/api/tickers":      lambda _qs: handle_tickers(),
    "/api/kase_test":    lambda qs: handle_kase_test(qs),
    "/api/export":       lambda qs: handle_export(qs),
<<<<<<< HEAD
    "/api/export/dcf":   lambda qs: handle_export_dcf(qs),
=======
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
}

_POST_ROUTES: dict = {
    "/api/fetch": lambda qs: handle_fetch_post(qs),
    "/api/stop":  lambda _qs: handle_stop_post(),
    "/api/clear": lambda _qs: handle_clear_post(),
}


<<<<<<< HEAD
def _clean_json(o):
    """Рекурсивно заменяем Infinity/NaN на null — они невалидны в JSON."""
    if isinstance(o, float):
        return None if (math.isinf(o) or math.isnan(o)) else o
    if isinstance(o, dict):
        return {k: _clean_json(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_clean_json(v) for v in o]
    return o


=======
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()}  {fmt % args}")

<<<<<<< HEAD
    def _send_json(self, obj: dict, status: int = 200) -> None:
        body = json.dumps(_clean_json(obj), ensure_ascii=False, default=str).encode()
=======
    # ── Утилиты ───────────────────────────────────────────────────────────────

    def _send_json(self, obj: dict, status: int = 200) -> None:
        import math

        def _clean(o):
            """Рекурсивно заменяем Infinity/NaN на null — они невалидны в JSON."""
            if isinstance(o, float):
                if math.isinf(o) or math.isnan(o):
                    return None
                return o
            if isinstance(o, dict):
                return {k: _clean(v) for k, v in o.items()}
            if isinstance(o, list):
                return [_clean(v) for v in o]
            return o

        body = json.dumps(_clean(obj), ensure_ascii=False, default=str).encode()
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
        self.send_response(status)
        self.send_header("Content-Type",   "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

<<<<<<< HEAD
    def _send_xlsx(self, body: bytes, filename: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Expose-Headers", "Content-Disposition")
        self.end_headers()
        self.wfile.write(body)

    def _serve_static(self, url_path: str) -> None:
        file_path = _resolve_file(url_path)
=======
    def _serve_static(self, url_path: str) -> None:
        file_path = _resolve_file(url_path)

>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
        if file_path:
            ext  = os.path.splitext(file_path)[1].lower()
            mime = MIME_TYPES.get(ext, "application/octet-stream")
            with open(file_path, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type",   mime)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
<<<<<<< HEAD
            print(f"  404: {url_path!r}")
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self) -> None:
        """Preflight CORS для браузерных запросов."""
=======
            # Подробный лог чтобы понять почему файл не найден
            tried = []
            for pfx, d in _URL_TO_DIR:
                if url_path.startswith(pfx):
                    fn = url_path[len(pfx):].replace("..", "").lstrip("/")
                    tried.append(os.path.join(_project_root, d, fn))
            print(f"  404 static: {url_path!r}")
            print(f"  root={_project_root!r}")
            for p in tried:
                print(f"  tried: {p!r} exists={os.path.isfile(p)}")
            self.send_response(404)
            self.end_headers()

    # ── Методы HTTP ───────────────────────────────────────────────────────────

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_OPTIONS(self) -> None:
        """Preflight CORS для браузерных запросов (Excel download)."""
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        qs     = parse_qs(parsed.query)

        handler = _GET_ROUTES.get(parsed.path)
        if not handler:
            self._serve_static(parsed.path)
            return

        try:
            result = handler(qs)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self._send_json({"error": str(exc)}, 500)
            return

<<<<<<< HEAD
        # Бинарные ответы: (status, bytes, content_type)
        if len(result) == 3:
            status, body, _ctype = result
            if isinstance(body, bytes) and status == 200:
                fname = f"export_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.xlsx"
                try:
                    self._send_xlsx(body, fname)
                except Exception:
                    pass
                return
            err = body if isinstance(body, dict) else {"error": body.decode("utf-8", errors="replace")}
            self._send_json(err, status)
=======
        # handle_export возвращает (status, bytes, content_type)
        if len(result) == 3:
            status, body, ctype = result
            if isinstance(body, bytes) and status == 200:
                from datetime import datetime
                fname = f"screener_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.xlsx"
                try:
                    self.send_response(200)
                    self.send_header("Content-Type", ctype)
                    self.send_header("Content-Disposition", f'attachment; filename="{fname}"')
                    self.send_header("Content-Length", str(len(body)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Access-Control-Expose-Headers", "Content-Disposition")
                    self.end_headers()
                    self.wfile.write(body)
                except Exception:
                    pass
                return
            # 4xx / 5xx от export
            err_body = body if isinstance(body, dict) else \
                       {"error": body.decode("utf-8", errors="replace")}
            self._send_json(err_body, status)
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
        else:
            status, body = result
            self._send_json(body, status)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        qs     = parse_qs(parsed.query)

        handler = _POST_ROUTES.get(parsed.path)
        if handler:
<<<<<<< HEAD
            try:
                status, body = handler(qs)
            except Exception as exc:
                import traceback
                traceback.print_exc()
                self._send_json({"error": str(exc)}, 500)
                return
=======
            status, body = handler(qs)
>>>>>>> 48fe0a82dc8de8e4b1571d8dc69fbb5300300ae0
            self._send_json(body, status)
        else:
            self.send_response(404)
            self.end_headers()


def create_server(host: str, port: int) -> ThreadingHTTPServer:
    """Создать и вернуть многопоточный HTTPServer."""
    return ThreadingHTTPServer((host, port), Handler)
