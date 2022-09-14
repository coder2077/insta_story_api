from redis import Redis
from .config import load_config


config = load_config()
# r = Redis(host=config.redis.host, port=config.redis.port, password=config.redis.password)
r = Redis(host='redis-12852.c261.us-east-1-4.ec2.cloud.redislabs.com', port=12852, password='Andrax_07')
