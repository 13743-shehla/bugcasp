"""Bound request bodies even when a client omits Content-Length."""
from starlette.responses import JSONResponse

class BodyLimitMiddleware:
    def __init__(self, app, max_bytes):
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http' or scope['method'] not in {'POST', 'PUT', 'PATCH'}:
            return await self.app(scope, receive, send)
        chunks = []
        size = 0
        while True:
            message = await receive()
            if message['type'] == 'http.disconnect':
                return
            chunk = message.get('body', b'')
            size += len(chunk)
            if size > self.max_bytes:
                response = JSONResponse({'detail': 'Request is too large.'}, status_code=413)
                return await response(scope, receive, send)
            chunks.append(chunk)
            if not message.get('more_body', False):
                break
        body = b''.join(chunks)
        delivered = False
        async def replay():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {'type': 'http.request', 'body': body, 'more_body': False}
            return await receive()
        await self.app(scope, replay, send)
