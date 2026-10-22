#!/usr/bin/env python3
"""Servidor local de teste: python3 tools/servir.py. Abra http://localhost:8080/."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, '.wasm': 'application/wasm', '.js': 'application/javascript', '.gz': 'application/gzip'}

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parents[1] / 'build/web')
    args = parser.parse_args()
    if not (args.directory / 'sw.js').exists():
        parser.error('Compile primeiro com python3 tools/compilar.py.')
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(args.directory)))
    print(f'Typica PWA: http://localhost:{args.port}/ (Ctrl+C para encerrar)', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
