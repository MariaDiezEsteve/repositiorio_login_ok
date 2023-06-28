class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'

class DevelopmentConfig():
    MYSQL_HOST = "containers-us-west-59.railway.app"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "mzj8vF2N8BRe4h8m8cyB"
    MYSQL_DB = "railway"
    MYSQL_PORT = 5906

config={
    "development": DevelopmentConfig
}