import pymysql
from itertools import chain

class get_Data():
    conn = pymysql.connect('localhost', 'xxx', 'xxx', 'zufang')

    def get_Rent_Section(self):     #各租金价格区间的房源数量
        cursor = self.conn.cursor()
        sql = """
            SELECT
            SUM(
                case
                when zf.rent <= 1000 then 1 else 0
                end
            ) ,
            SUM(
                case
                when zf.rent > 1000 and zf.rent <= 2000 then 1 else 0
                end
            ) ,
            SUM(
                case
                when zf.rent > 2000 and zf.rent <= 3000 then 1 else 0
                end
            ) ,
            SUM(
                case
                when zf.rent > 3000 and zf.rent <= 4000 then 1 else 0
                end
            ) ,
            SUM(
                case
                when zf.rent > 4000 and zf.rent <= 5000 then 1 else 0
                end
            ) ,
            SUM(
                case
                when zf.rent > 5000 and zf.rent <= 6000 then 1 else 0
                end
            ) ,
            SUM(
                case
                when zf.rent > 6000 then 1 else 0
                end
            )
            from zf
            """
        cursor.execute(sql)
        data = cursor.fetchall()
        resultlist = list(chain.from_iterable(data))

        cursor.close()
        self.conn.commit()

        return resultlist

    def get_Unit_Num_Ratio(self):   #各地区房屋数量和各地区单位面积租金比
        cursor = self.conn.cursor()
        sql = """
            Select zf.address,COUNT(id) as `房屋数量`,
            CONVERT(SUM(rent)/SUM(area),DECIMAL(10,2)) as `单位面积租金价格`
            from zf
            where zf.rent < 10000 and zf.area < 1000
            GROUP BY zf.address
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        resultlist = list(chain.from_iterable(data))

        cursor.close()
        self.conn.commit()
        return resultlist

    def get_Region_Rent(self):     #各地区房屋租金分布
        cursor = self.conn.cursor()
        resultlist = []

        sql = """
            Select zf.rent
            from zf
            where zf.rent < 10000 and zf.area < 1000
            AND zf.address = '从化'
        """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        sql = """
                    Select zf.rent
                    from zf
                    where zf.rent < 10000 and zf.area < 1000
                    AND zf.address = '南沙'
                """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        sql = """
                    Select zf.rent
                    from zf
                    where zf.rent < 10000 and zf.area < 1000
                    AND zf.address = '增城'
                """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        sql = """
                    Select zf.rent
                    from zf
                    where zf.rent < 10000 and zf.area < 1000
                    AND zf.address = '天河'
                """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        sql = """
                    Select zf.rent
                    from zf
                    where zf.rent < 10000 and zf.area < 1000
                    AND zf.address = '海珠'
                """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        sql = """
                    Select zf.rent
                    from zf
                    where zf.rent < 10000 and zf.area < 1000
                    AND zf.address = '番禺'
                """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        sql = """
                    Select zf.rent
                    from zf
                    where zf.rent < 10000 and zf.area < 1000
                    AND zf.address = '白云'
                """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        sql = """
                    Select zf.rent
                    from zf
                    where zf.rent < 10000 and zf.area < 1000
                    AND zf.address = '花都'
                """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        sql = """
                    Select zf.rent
                    from zf
                    where zf.rent < 10000 and zf.area < 1000
                    AND zf.address = '荔湾'
                """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        sql = """
                    Select zf.rent
                    from zf
                    where zf.rent < 10000 and zf.area < 1000
                    AND zf.address = '越秀'
                """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        sql = """
                    Select zf.rent
                    from zf
                    where zf.rent < 10000 and zf.area < 1000
                    AND zf.address = '黄埔'
                """
        cursor.execute(sql)
        data = list(chain.from_iterable(cursor.fetchall()))
        resultlist.append(data)

        cursor.close()
        self.conn.commit()
        return resultlist

    def get_Room_Hall(self):       #房屋室厅
        cursor = self.conn.cursor()
        sql = """
            Select zf.room,zf.hall,Count(*)
            from zf
            where zf.area<1000 and zf.rent<10000 and room > 0 and room < 4
            group by zf.room,zf.hall
        """

        cursor.execute(sql)
        data = cursor.fetchall()
        resultlist = list(chain.from_iterable(data))

        cursor.close()
        self.conn.commit()
        return resultlist

    def get_Orientations(self):     #房屋朝向
        cursor = self.conn.cursor()
        sql = """
            Select zf.orientations,Count(*)
            from zf
            where zf.area<1000 and zf.rent<10000 and room > 0 and room < 4 and zf.orientations <> 'Nostr'
            Group by zf.orientations
        """

        cursor.execute(sql)
        data = cursor.fetchall()
        resultlist = list(chain.from_iterable(data))

        cursor.close()
        self.conn.commit()
        return resultlist

    def get_Note_one(self):     #小区管理
        cursor = self.conn.cursor()
        sql = """
            Select Count(*) from zf
            where note_one = '小区管理' or note_two = '小区管理' or note_three = '小区管理'
        """

        cursor.execute(sql)
        data = cursor.fetchall()
        resultlist = list(chain.from_iterable(data))

        cursor.close()
        self.conn.commit()
        return resultlist

    def get_Note_two(self):     #拎包入住
        cursor = self.conn.cursor()
        sql = """
            Select Count(*) from zf
            where note_one = '拎包入住' or note_two = '拎包入住' or note_three = '拎包入住'
        """

        cursor.execute(sql)
        data = cursor.fetchall()
        resultlist = list(chain.from_iterable(data))

        cursor.close()
        self.conn.commit()
        return resultlist

    def get_all_data(self):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
                select * from zf
                where zf.subway <> '-1'
                and zf.note_one <> 'no'
                and zf.note_two <> 'no'
                and zf.note_three <> 'no' 
                LIMIT 100
            """
        cursor.execute(sql)
        rs = cursor.fetchall()

        cursor.close()
        return rs

    def close_Conn(self):
        self.conn.close()




