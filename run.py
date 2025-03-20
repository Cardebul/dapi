import uvicorn
from asgiref.wsgi import WsgiToAsgi

from app.main import app

asgi_app = WsgiToAsgi(app)
    
def apply_migrations():
    from alembic import command, config
    alembic_cfg = config.Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    apply_migrations()
    uvicorn.run(asgi_app, host="0.0.0.0", port=8000)