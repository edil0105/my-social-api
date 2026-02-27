import pymysql
from django.db.backends.base.base import BaseDatabaseWrapper

# 1. MySQLdb орнына pymysql-ді қолдану
pymysql.install_as_MySQLdb()

# 2. Нұсқаны тексеру функциясын бос функциямен алмастыру (Monkeypatching)
def stub_check_version(*args, **kwargs):
    return []

BaseDatabaseWrapper.check_database_version_supported = stub_check_version