from flask import Flask
from flask_mongoengine import MongoEngine
from flask_rabmq import RabbitMQ

from app.config import Config


db = MongoEngine()
ramq = RabbitMQ()

def create_app(config_filename=None):
    
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ramq.init_app(app=app)
    ramq.run_consumer()
    with app.app_context():
        from app.api.task import task_bp
        app.register_blueprint(task_bp)
        return app
 