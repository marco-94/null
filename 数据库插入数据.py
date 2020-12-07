import pymysql
import time

coon = pymysql.connect(host='rm-wz9104odexj715182yo.mysql.rds.aliyuncs.com', port=3306, user='common_callcenter',
                       passwd='~&q5A2DV3p', db='common_callcenter_15')
cursor = coon.cursor()
for j in range(11, 16):
    for i in range(0, 200000):
        create_tm = str(round(time.time() * 1000))
        last_update_tm = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('INSERT INTO `request_record_' + str(
            j) + '` (id, city_code, agent_phone, answered_phone, virtual_phone, binding_code, supplier, CODE, msg, model_type, extra, create_tm, last_update_tm) VALUES("' + str(
            j) + '88888900' + str(
            i) + '", "440100", "19163881627", "19163881727", "18620416596", "DX020X202011131752426655474-6-1-YJYCT-GX", "1", "10000", "请求成功", "bindXB", "{}", "' + create_tm + '", "' + last_update_tm + '");')
        print(i)
        coon.commit()
coon.close()
cursor.close()
