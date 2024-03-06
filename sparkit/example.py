from pyspark.sql import DataFrame, SparkSession

# Create the Spark Session
spark = SparkSession.builder \
    .appName("example") \
    .config("spark.driver.host", "localhost") \
    .master("local") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
spark.conf.set("spark.sql.shuffle.partitions", "5")

df: DataFrame = spark.read \
    .option("header", True) \
    .csv("testusers.csv")

df_users = df.createOrReplaceTempView('users')

def getAllUsers() -> DataFrame:
    sql = 'SELECT * FROM users'
    return spark.sql(sql)

print("All users:")
getAllUsers().show()

def getAllTitle() -> DataFrame:
    sql = '''
    SELECT 
        Title,
        COUNT(Title) AS titleCount
    FROM users
    GROUP BY Title
    '''
    return spark.sql(sql)
print("All title:")
print(getAllTitle().show())