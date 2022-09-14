import configparser
from dataclasses import dataclass



VERSION = '1.0.0'


@dataclass
class Key:
	secret: str


@dataclass
class RedisDB:
	host: str
	port: int
	password: str
	db: str


@dataclass
class Config:
	key: Key
	redis: RedisDB


def load_config():
	config = configparser.ConfigParser()
	config.read('config.ini')
	key = config["key"]
	redis = config["redis"]

	return Config(
		key=Key(
			secret=key["secret-key"]
		), 
		redis=RedisDB(
			host=redis['host'], 
			port=redis['port'], 
			password=redis['password'], 
			db=redis['db']
		), 
	)
