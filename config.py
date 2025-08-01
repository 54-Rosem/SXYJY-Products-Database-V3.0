import os

# 项目根目录路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """配置类，用于存储项目的所有配置信息"""

    # 配置数据库连接
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用对象修改追踪，提高性能

    # 上传文件夹路径
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

