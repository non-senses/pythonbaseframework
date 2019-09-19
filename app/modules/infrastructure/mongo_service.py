from mongoengine import connect
from config import getDbConfig

mongoSettings = getDbConfig()['mongo-default']

print(mongoSettings)

dbConnection = connect(**mongoSettings)
