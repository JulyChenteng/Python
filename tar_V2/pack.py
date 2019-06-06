# -*- coding: utf-8 -*-
import configparser
import os
import tarfile
import time
import datetime
import re

CONFIG_FILE = "pack.cfg"

'''
    ��ʼ������
'''
def init_config(fileName):
    if os.path.exists( os.path.join(os.getcwd(),fileName) ):
        conf = configparser.ConfigParser()
        conf.read(fileName)
        return conf
    
    return -1

'''
    ��ȡ����������
'''
def read_common_options(conf):
    maxSerial = conf.get("COMMON", "MAX_SERIAL_NO")
    maxSerialNo = int(re.sub("\\D","", maxSerial))

    maxTarSizeExpr = conf.get("COMMON", "MAX_TARFILE_SIZE")
    maxTarFileSize = eval(maxTarSizeExpr.lstrip().rstrip()) 

    duration = conf.get("COMMON", "TIME_WAIT")
    timeWait = int(re.sub("\\D","", duration))

    return maxSerialNo, maxTarFileSize, timeWait

'''
ƴ��ѹ�����ļ���
�����淶��
    �굥����(gprs;sms;gsm)_������(0001~9999)_�����ʼʱ��(YYYYMMDDHHmm).tar
'''
def get_package_name(packagePath, recordType, nCount, tmBegin ):
    pattern =  '{0:04d}'
    serialNo = pattern.format(nCount)
    strTmBegin = tmBegin.strftime("%Y%m%d%H%M")    
    packageName = packagePath + "/" + recordType + "_" + serialNo + "_" + strTmBegin + ".tar"
    
    return packageName

def run(conf, recordType):
    print("Process ", recordType, "record begin...")

    # ��ȡ�굥·���Լ�ѹ��������·��
    recordPath = conf.get(recordType, "RECORD_PATH")
    packagePath = conf.get(recordType, "PACKAGE_PATH")

    if not os.path.exists(packagePath):
        os.mkdir(packagePath)

    if not os.path.exists(recordPath):
        print("The record path is not exist!\n")
        return

    maxSerialNo, maxTarFileSize, timeWait = read_common_options(conf)

    currPath = os.getcwd()
    recordPath = os.path.join(currPath, recordPath)
    packagePath = os.path.join(currPath, packagePath)
    
    os.chdir(recordPath)
    nCount = 0
    nTarFileSize = 0

    # ����Ŀ¼��ȡ�ļ��б�
    for _, _, fileList in os.walk(recordPath):
        tmBegin = datetime.datetime.now()
        packageName = get_package_name(packagePath, recordType, nCount, tmBegin)
        tar = tarfile.open(packageName, 'w:gz')

        # �����ļ��б�
        os.chdir(recordPath)
        for fileName in fileList:
            if os.path.isfile(fileName):
                if nCount > maxSerialNo:
                    nCount %= maxSerialNo + 1

                tmTmp = datetime.datetime.now() 
                
                nTarFileSize += os.path.getsize(fileName)

                # ѹ����Դ�ļ������������ֵ���ߴ�������ѵ�
                if nTarFileSize > maxTarFileSize or (tmTmp-tmBegin).seconds >= timeWait:
                    tar.close()
                    nCount += 1
                    nTarFileSize = os.path.getsize(fileName)

                    # ѹ����Դ�ļ������������ֵ���Ǵ������δ��������ȴ�
                    if timeWait - (tmTmp-tmBegin).seconds > 0:
                        print(timeWait - (tmTmp-tmBegin).seconds)
                        time.sleep(timeWait - (tmTmp-tmBegin).seconds)
                    
                    tmBegin = datetime.datetime.now()
                    packageName = get_package_name(packagePath, recordType, nCount, tmBegin)
                    tar = tarfile.open(packageName, 'w:gz') 
                tar.add(fileName)
                
        if not tar.closed:
            tar.close()
        os.chdir(currPath)

    print("Process ", recordType, "record end...\n")        

def main():
    conf = init_config(CONFIG_FILE)
    if -1 == conf:
        print("The config file is not exist!")
        return

    run(conf, "GPRS")
    run(conf, "GSM")
    run(conf, "SMS")

if __name__ == "__main__":
    main()
    
