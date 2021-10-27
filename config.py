from decouple import config


class Config(object):
    SECRET_KEY = config('SECRET_KEY') or 'guess-me'
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    # EMAIL SETTINGS
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_DEBUG = True
    MAIL_USERNAME = 'replace.it.with.working.mail@gmail.com'
    MAIL_PASSWORD = 'replace_it_with_correct_password'
    
    # OR USE

    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_DEBUG = True
    # MAIL_USERNAME = 'replace.it.with.working.mail@gmail.com'
    # MAIL_PASSWORD = 'replace_it_with_correct_password'


class ProductionConfig(Config):
    DEBUG = False
    MAIL_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
