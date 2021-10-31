
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

filename="hdfs://localhost:9000/user/hadoop/input/zuf2.csv"
homefile="file:///home/hadoop/文档/zuf2.csv"
class zufang_pyspark():
    def __init__(self):
        self.spark = SparkSession \
            .builder \
            .appName("zuFang pySpark") \
            .config("spark.some.config.option", "some-value") \
            .getOrCreate()
        self.df =self.spark.read.csv(homefile, header=True)
        # df=spark.read.format('com.databricks.spark.csv'). \
        #     options(header='true',inferschema='true',). \
        #     load(homefile, header=True)

    def get_Data(self):
        df=self.df
        df=df.filter(df.rent<=6000)
        return df

    def get_Rent_Section(self,df):              #各租金价格区间的房源数量

        resultlist=[2 for _ in range(6)]
        resultlist[0] = df.filter(df.rent < 1000).count()
        resultlist[1] = df.filter(df.rent > 1000).filter(df.rent < 2000).count()
        resultlist[2] = df.filter(df.rent > 2000).filter(df.rent < 3000).count()
        resultlist[3] = df.filter(df.rent > 3000).filter(df.rent < 4000).count()
        resultlist[4] = df.filter(df.rent > 4000).filter(df.rent < 5000).count()
        resultlist[5] = df.filter(df.rent > 5000).filter(df.rent <=6000).count()
        return resultlist

    def get_Region_Rent(self,df):  # 各地区房屋租金分布
        """
        resultlist[0从化,1南沙,2增城,3天河,4海珠,5番禺,6白云,7花都,8荔湾,9越秀,10黄埔]
        """
        resultlist = [[] for _ in range(11)]
        resultlist[0] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '从化').collect()]
        resultlist[1] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '南沙').collect()]
        resultlist[2] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '增城').collect()]
        resultlist[3] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '天河').collect()]
        resultlist[4] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '海珠').collect()]
        resultlist[5] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '番禺').collect()]
        resultlist[6] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '白云').collect()]
        resultlist[7] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '花都').collect()]
        resultlist[8] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '荔湾').collect()]
        resultlist[9] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '越秀').collect()]
        resultlist[10] = [_['rent'] for _ in df.filter(df.area < 1000).filter(df.address == '黄埔').collect()]
        return resultlist

    def get_Room_Hall(self,df):       #房屋室厅
        resultlist=[_ for _ in df.filter(df.area < 1000).filter(df.room > 0).filter(df.room < 4).groupBy(df.room , df.hall).count().collect()]
        return resultlist

    def get_Orientations(self,df):     #房屋朝向
        resultlist = [_ for _ in df.filter(df.area < 1000).filter(df.room > 0).filter(df.room < 4).groupBy(df.orientations).count().collect()]
        return resultlist

    def get_Note_one(self,df):  # 小区管理
        resultlist = df.filter((df.note_one == '小区管理') | (df.note_two == '小区管理') | (df.note_three == '小区管理')).count()
        print(resultlist)

    def get_Note_two(self,df):  # 拎包入住
        resultlist = df.filter((df.note_one == '拎包入住') | (df.note_two == '拎包入住') | (df.note_three == '拎包入住')).count()
        print(resultlist)


    def data_show(self,df):
        df.describe(['rent']).show()
        # df.show()

    def pyspark_stop(self):
        self.spark.stop()

zf=zufang_pyspark()
df=zf.get_Data()
# zf.get_Note_one(df)
zf.get_Note_two(df)
# zf.data_show(df=df)
zf.pyspark_stop()