import pymysql
coon = pymysql.connect(host='', port=3306, user='', passwd='', db='')
cursor = coon.cursor()
for i in range(20000, 30000):
    ids = str(0+i)
    cursor.execute('')
coon.commit()
coon.close()
cursor.close()




