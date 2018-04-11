import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ General configuration """
    # TODO: Configutation
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = ""
    # It significant overhead and will be disabled by default in the future.
    # Set SQLALCHEMY_TRACK_MODIFICATIONS False to suppress this warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """ Debug configuration """
    DEBUG = True


class TestingConfig(Config):
    """ Testing configuration """
    TESTING = True


class ProductionConfig(Config):
    """ Production configuration """


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 默认是开发设置
    'default': DevelopmentConfig
}
