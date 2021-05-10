import os

class Config:
    
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASS = os.getenv("MONGO_PASS")
    
    RABBIT_USER = os.getenv("RABBIT_USER")
    RABBIT_PASS = os.getenv("RABBIT_PASS")
    RABBIT_VHOST = os.getenv("RABBIT_VHOST")
    
    MONGODB_SETTINGS = {
        "host": f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongo:27017/examples?authSource=admin",
        "alias": "default"
    }
    RABMQ_RABBITMQ_URL = f"amqp://{RABBIT_USER}:{RABBIT_PASS}@rabbit:5672/{RABBIT_VHOST}"
    RABMQ_SEND_EXCHANGE_NAME = "flask_rabmq"
    RABMQ_SEND_EXCHANGE_TYPE = "topic"
    RABMQ_SEND_POOL_ACQUIRE_TIMEOUT = 5
