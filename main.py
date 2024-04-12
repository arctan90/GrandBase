from fastapi import FastAPI, WebSocket
from component.processor import *
import os

app = FastAPI()

websocket_connections = []

handlers = {
    'register': p_register,
    'createSatellite': p_create_satellite,
    'forward': p_forward,
}


@app.websocket("/ws/conn")
async def websocket_endpoint(websocket: WebSocket):
    # 将连接添加到列表中
    await websocket.accept()
    websocket_connections.append(websocket)
    try:
        # 等待消息
        while True:
            data = await websocket.receive_json()
            mid = data['mid']

            handler = handlers.get(mid)
            if handler is None:
                await websocket.send_json({"code": 403, "message": "invalid mid"})
                continue
            toSend = handler(data)

            await websocket.send_json(toSend)
    except Exception as e:
        msg = f"WebSocket connection closed: {e}"
        await websocket.send_json({"code": 503, "message": msg})
    finally:
        # 从列表中移除关闭的连接
        websocket_connections.remove(websocket)


if __name__ == '__main__':
    svc_port = os.getenv("SVC_PORT", 8000)

    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=svc_port)