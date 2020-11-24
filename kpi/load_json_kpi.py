
# coding: UTF-8

import sys
import traceback
import shutil
import Queue
import threading

from common import *

bRun = False
stopping = threading.Event()

biz_queue = {}
fields_map = {
    "cg_fields": "SERV_ID,TIME,ONREQUEST_COST_COUNT,ONREQUEST_COST_AVERAGE,ONREQUEST_COST_MIN_COST,ONREQUEST_COST_MAX_COST,DECODE_COST_COUNT,DECODE_COST_AVERAGE,DECODE_COST_MIN_COST,DECODE_COST_MAX_COST,SESSION_COST_COUNT,SESSION_COST_AVERAGE,SESSION_COST_MIN_COST,SESSION_COST_MAX_COST,CG_GATEWAY_COST_COUNT,CG_GATEWAY_COST_AVERAGE,CG_GATEWAY_COST_MIN_COST,CG_GATEWAY_COST_MAX_COST,ONRESPONSE_COST_COUNT,ONRESPONSE_COST_AVERAGE,ONRESPONSE_COST_MIN_COST,ONRESPONSE_COST_MAX_COST,WRITEFILE_COST_COUNT,WRITEFILE_COST_AVERAGE,WRITEFILE_COST_MIN_COST,WRITEFILE_COST_MAX_COST,CG_GATEWAY_REV_COST_CNT,CG_GATEWAY_REV_COST_AVR,CG_GATEWAY_REV_COST_MIN_COST,CG_GATEWAY_REV_COST_MAX_COST,ENCODE_COST_COUNT,ENCODE_COST_AVERAGE,ENCODE_COST_MIN_COST,ENCODE_COST_MAX_COST,REQUEST_COUNT,REQUEST_OK_COUNT,REQUEST_FAIL_COUNT,RESPONSE_COUNT,RESPONSE_OK_COUNT,RESPONSE_DIRECT_COUNT,RESPONSE_TIMEOUT_COUNT,CG_GENERATOR_COST_COUNT,CG_GENERATOR_COST_AVERAGE,CG_GENERATOR_COST_MIN_COST,CG_GENERATOR_COST_MAX_COST,CG_GENERATOR_COUNT,CG_COST_COUNT,CG_COST_AVERAGE,CG_COST_MIN_COST,CG_COST_MAX_COST,RF_COST_COUNT,RF_COST_AVERAGE,RF_COST_MIN_COST,RF_COST_MAX_COST,SEND_RF_FAIL,POPACKSDL_COST_COUNT,POPACKSDL_COST_AVERAGE,POPACKSDL_COST_MIN_COST,POPACKSDL_COST_MAX_COST,POPREQ_COST_COUNT,POPREQ_COST_AVERAGE,POPREQ_COST_MIN_COST,POPREQ_COST_MAX_COST,POPACK_COST_COUNT,POPACK_COST_AVERAGE,POPACK_COST_MIN_COST,POPACK_COST_MAX_COST,INSOCK_COST_COUNT,INSOCK_COST_AVERAGE,INSOCK_COST_MIN_COST,INSOCK_COST_MAX_COST", 
    'cg_placeholders': ":SERV_ID,:TIME,:ONREQUEST_COST_COUNT,:ONREQUEST_COST_AVERAGE,:ONREQUEST_COST_MIN_COST,:ONREQUEST_COST_MAX_COST,:DECODE_COST_COUNT,:DECODE_COST_AVERAGE,:DECODE_COST_MIN_COST,:DECODE_COST_MAX_COST,:SESSION_COST_COUNT,:SESSION_COST_AVERAGE,:SESSION_COST_MIN_COST,:SESSION_COST_MAX_COST,:CG_GATEWAY_COST_COUNT,:CG_GATEWAY_COST_AVERAGE,:CG_GATEWAY_COST_MIN_COST,:CG_GATEWAY_COST_MAX_COST,:ONRESPONSE_COST_COUNT,:ONRESPONSE_COST_AVERAGE,:ONRESPONSE_COST_MIN_COST,:ONRESPONSE_COST_MAX_COST,:WRITEFILE_COST_COUNT,:WRITEFILE_COST_AVERAGE,:WRITEFILE_COST_MIN_COST,:WRITEFILE_COST_MAX_COST,:CG_GATEWAY_REV_COST_CNT,:CG_GATEWAY_REV_COST_AVR,:CG_GATEWAY_REV_COST_MIN_COST,:CG_GATEWAY_REV_COST_MAX_COST,:ENCODE_COST_COUNT,:ENCODE_COST_AVERAGE,:ENCODE_COST_MIN_COST,:ENCODE_COST_MAX_COST,:REQUEST_COUNT,:REQUEST_OK_COUNT,:REQUEST_FAIL_COUNT,:RESPONSE_COUNT,:RESPONSE_OK_COUNT,:RESPONSE_DIRECT_COUNT,:RESPONSE_TIMEOUT_COUNT,:CG_GENERATOR_COST_COUNT,:CG_GENERATOR_COST_AVERAGE,:CG_GENERATOR_COST_MIN_COST,:CG_GENERATOR_COST_MAX_COST,:CG_GENERATOR_COUNT,:CG_COST_COUNT,:CG_COST_AVERAGE,:CG_COST_MIN_COST,:CG_COST_MAX_COST,:RF_COST_COUNT,:RF_COST_AVERAGE,:RF_COST_MIN_COST,:RF_COST_MAX_COST,:SEND_RF_FAIL,:POPACKSDL_COST_COUNT,:POPACKSDL_COST_AVERAGE,:POPACKSDL_COST_MIN_COST,:POPACKSDL_COST_MAX_COST,:POPREQ_COST_COUNT,:POPREQ_COST_AVERAGE,:POPREQ_COST_MIN_COST,:POPREQ_COST_MAX_COST,:POPACK_COST_COUNT,:POPACK_COST_AVERAGE,:POPACK_COST_MIN_COST,:POPACK_COST_MAX_COST,:INSOCK_COST_COUNT,:INSOCK_COST_AVERAGE,:INSOCK_COST_MIN_COST,:INSOCK_COST_MAX_COST",

    "sg_fields": "",
    "sg_placeholders": "",
} 

def parse_cfg():
    ''' 获取配置
    '''
    # root = etree.parse(os.path.join(os.path.dirname(__file__), 'config.xml')).getroot()

    # user = root.xpath('db/user')[0].text
    # pwd = root.xpath('db/pwd')[0].text
    # dns = root.xpath('db/dns')[0].text
    # id_arr = root.xpath('db/biz_ids')[0].text
    user = "ud" 
    pwd = "ud" 
    dns = "jxcsbj1=(DESCRIPTION=(LOAD_BALANCE=OFF)(FAILOVER=ON)(ADDRESS=(PROTOCOL=TCP)(HOST=10.239.40.200)(PORT=1521))(ADDRESS=(PROTOCOL=TCP)(HOST=10.239.40.201)(PORT=1521))(CONNECT_DATA =(SERVER=DEDICATED)(SERVICE_NAME=jxcsbj)(FAILOVER_MODE=(TYPE=SELECT)(METHOD=BASIC)(RETRIES=180)(DELAY=5))))" 
    id_arr = "107"
	
    id_arr = id_arr.split(',')
    biz_ids = []
    for id in id_arr:
        biz_ids.append(int(id))

    return user, pwd, dns, biz_ids

def parse_sql(biz_ids):
    ''' 根据biz_id解析出对应的sql
    '''

    biz_sql = {}

    if len(biz_ids) == 0:
        logging.error('empty biz_ids, no need to process')
        return biz_sql, 0

    switcher = { 
        105: {'fields': fields_map['sg_fields'], 'placeholders': fields_map['sg_placeholders'], 'table': 'ocs_sg_kpi_log_5g'}, 
        107: {'fields': fields_map['cg_fields'], 'placeholders': fields_map['cg_placeholders'], 'table': 'ud.ocs_kpi_log_5g'}, 
    } 

    for biz_id in biz_ids:
        res = switcher.get(biz_id, -1)
        if res == -1:
            logger.error('error biz_id: ' + biz_id)
            continue
       
        sql = 'insert into ' + res['table'] + '(' + res['fields'] + ') values(' + res['placeholders'] + ')'
        #print(sql)
        logger.info('parse_sql: ' + sql)
        biz_sql[biz_id] = sql

    return biz_sql, len(biz_sql)

def process(kpi_path, bak_path, biz_ids):
    ''' kpi处理流程
    '''
    logger.info('kpi_path:' + kpi_path + ',bak_path:' + bak_path)

    all_files = os.listdir(kpi_path)
    for filename in all_files:
        filePath = os.path.join(kpi_path, filename)
	logger.info('process file: ' + filePath);
        _, size = kpi_process.parsefile(filePath, biz_ids, biz_queue)
        print(biz_queue[107])
	#print(biz_queue[107].get())
	if size == -1:
            logger.error('attention: input ' + filePath + ' is not a file')
            continue
        shutil.move(filePath, bak_path)
    stopping.set()

def load(conn, biz_sql, biz_id, stat_queue):
    ''' stat入库
    '''
    # print("111")
    while bRun :
        try:
            while not stat_queue.empty():
                tmp_stat = stat_queue.get()
		        # print(tmp_stat)
                sql = biz_sql[biz_id]
		        # print("222" + sql)
                conn.update(sql, tmp_stat)
        except BaseException:
            # 异常打印异常日志
            conn.rollback()
	        print("rollback")
	        exit()
            # traceback.print_exc()
            # logger.error('error occurred when insert data:[ ' + tmp_stat + ' ]')
	conn.commit()

        
	if stopping.is_set() and stat_queue.empty():
	    break

if __name__ == "__main__":
    # 必须两个参数，参数1为kpi文件路径，参数2为kpi备份路径
    if len(sys.argv) < 2:
        logger.error('usage: need two arguments — 1. kpi path 2. kpi bak path')
        exit()
    kpi_path = sys.argv[1]
    bak_path = sys.argv[2]

    bRun = True
    bOver = False

    db_conn = conn_oracle()

    # 1.初始化日志模块
    # 2.解析配置文件（主要是数据库，其他的后面再加）
    user, pwd, dsn, biz_ids = parse_cfg()
    logger.info('db_info — user:' + user + ', dsn:' + dsn)

    # 每个biz_id对应一个队列
    for biz_id in biz_ids:
        biz_queue[biz_id] = Queue.Queue(1000)

    # 3.初始化db连接
    dsn = cx_Oracle.makedsn('10.15.49.45', 1521, sid='jxcmc_v8'); 
    db_conn.connect(user, pwd, dsn)

    # 4.根据biz_ids解析出对应insert语句映射<biz_id, insertsql>
    biz_sql, size = parse_sql(biz_ids)
    if size == 0:
        exit()

    # 5.解析kpi文件、kpi记录入库
    threads = []
    # 第一个线程负责解析kpi文件放入kpi_queue
    threads.append( threading.Thread(target=process, args=(kpi_path, bak_path, biz_ids,)) )

    # 其他每个队列对应一个线程插入数据
    for biz_id, stat_queue in biz_queue.items():
	print(type(biz_id))
	thread = threading.Thread(target=load, args=(db_conn, biz_sql, biz_id, stat_queue,))
        threads.append(thread)
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
    bRun = False
    bOver = True

    # 6.关闭连接
    if db_conn:
        db_conn.close()
