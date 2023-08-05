import os
from typing import Optional

from pyspark.sql import SparkSession


def get_spark_logger(spark: SparkSession, name: Optional[str] = None):
    log4j_logger = spark._jvm.org.apache.log4j  # noqa
    if name is None:
        name = os.path.basename(__file__)

    return log4j_logger.LogManager.getLogger("pyspark." + name)