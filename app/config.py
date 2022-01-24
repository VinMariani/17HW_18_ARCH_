class Config:
    DEBUG = True
    # SECRET - ключи, настройки внешних интеграций
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
