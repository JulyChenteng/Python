# -*- coding: utf-8 -*-
import configparser
import os
import tarfile
import time
import datetime
import threading
import re
import shutil

CONFIG_FILE = "pack.cfg"

'''
    初始化配置
'''
def init_config(fileName):
    if os.path.exists( os.path.join(os.getcwd(),fileName) ):
        conf = configparser.ConfigParser()
        conf.read(fileName)
        return conf
    
    return -1

'''
    读取公共配置项
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
    统计压缩包信息，获取压缩包里的文件个数、文件总大小和文件名列表
'''
def stat(packageName):
    nCount = 0
    nTotalSize = 0
    tf = tarfile.open(packageName, "r:gz")
    
    for ti in tf:
        if ti.isfile():
            nTotalSize += ti.size
    
    return len(tf.getnames()), nTotalSize, tf.getnames()

'''
拼接压缩包文件名
命名规范：
    详单种类(gprs;sms;gsm)_打包序号(0001~9999)_打包开始时间(YYYYMMDDHHmm).tar
'''
def get_package_name(packagePath, recordType, nCount, tmBegin ):
    pattern =  '{0:04d}'
    serialNo = pattern.format(nCount)
    strTmBegin = tmBegin.strftime("%Y%m%d%H%M%S")    
    packageName = packagePath + "/" + recordType + "_" + serialNo + "_" + strTmBegin + ".tar"
    
    return packageName

def run(conf, recordType):
    print("Process " + recordType, "record thread begin...")

    # 获取详单路径以及压缩包保存路径
    recordPaths = conf.get(recordType, "RECORD_PATH")
    packagePath = conf.get(recordType, "PACKAGE_PATH")
    bakPath = conf.get(recordType, "BAK_PATH")
    
    print("RECORD_PATH: " + recordPaths)
    print("PACKAGE_PATH: " + packagePath)
    print("BAK_PATH: " + bakPath)

    if not os.path.exists(bakPath):
        print("The package path is not exist")
        return

    if not os.path.exists(packagePath):
        print("The bak path is not exist!")
        return

    packageTmpPath = os.path.join(packagePath, 'tmp_dir')
    if not os.path.exists(packageTmpPath):
        print("The path '" + packageTmpPath + "' is not exist!")
        return

    strTm = datetime.datetime.now().strftime("%Y%m%d")
    bakPath = os.path.join(bakPath, strTm)
    if not os.path.exists(bakPath):
        os.mkdir(bakPath)

    # 支持详单输入路径存在多个目录的情况
    recordPathList = recordPaths.split(';')
    print(recordPathList)

    maxSerialNo, maxTarFileSize, timeWait = read_common_options(conf)
    currPath = os.getcwd()

    nCount = 0          # 包个数
    nFileCount = 0      # 应该打进包的原文件个数
    nTarFileSize = 0    # 包中原文件总大小
    isDirEmpty = True

    tmBegin = datetime.datetime.now()
    packageName = get_package_name(packageTmpPath, recordType, nCount, tmBegin)
    tar = tarfile.open(packageName, 'w:gz')
    for recordPath in recordPathList:
        if not os.path.exists(recordPath):
            print("The record path is not exist!\n")
            return

        recordPath = os.path.join(currPath, recordPath)
        packageTmpPath = os.path.join(currPath, packageTmpPath)
        packagePath = os.path.join(currPath, packagePath)
        bakPath = os.path.join(currPath, bakPath)
        
        # 遍历目录获取文件列表
        fileList = os.listdir(recordPath)

        if fileList:
            for file in fileList:
                fileName = os.path.join(recordPath, file)

                if os.path.isfile(fileName):
                    if nCount > maxSerialNo:
                        nCount %= maxSerialNo + 1

                    # 单个文件大于MAX_TARFILE_SIZE，过滤掉，不参与压缩
                    if os.path.getsize(fileName) > maxTarFileSize:
                        print("Exception: Filter " + fileName + ", file size = ", os.path.getsize(fileName), " greater than MAX_TAR_FILE_SIZE.")
                        continue

                    # 放在单个大于MAX_TARFILE_SIZE情况之后，可以解决以下情况：
                    # 当目录下所有文件都大于MAX_TARFILE_SIZE时，出空包的情况
                    isDirEmpty = False    
                    
                    tmTmp = datetime.datetime.now() 
                    nTarFileSize += os.path.getsize(fileName)
                
                   # 压缩包源文件总量大于最大值或者打包周期已到
                    if nTarFileSize > maxTarFileSize or (tmTmp-tmBegin).seconds >= timeWait:
                        tar.close()
                        
                        nTarFileSize -= os.path.getsize(fileName)
                        nRealCount, nTotalTarFileSize, fileNameList = stat(packageName)
                        if nFileCount != nRealCount or nTarFileSize != nTotalTarFileSize:
                            print("Error: file name is " + packageName, ", Total number of original files =", 
                            nFileCount, ", The total number of files in the tar file =", nRealCount, 
                            ", Total size of original files =", nTarFileSize, ", Total size of files in the tar file = ",
                            nTotalTarFileSize, "Files: ",  fileNameList) 
                        else:
                            print("Success: file name is ",  packageName, ", Total number of original files =",
                            nFileCount, ", The total number of files in the tar file =", nRealCount,
                            ", Total size of original files =", nTarFileSize, ", Total size of files in the tar file = ",
                            nTotalTarFileSize, ", Files: ",  fileNameList)
 
                        shutil.move(packageName, packagePath)

                        nCount += 1
                        nFileCount = 0
                        nTarFileSize = os.path.getsize(fileName)
                        
                        # 压缩包源文件总量大于最大值但是打包周期未结束，则等待
                        if timeWait - (tmTmp-tmBegin).seconds > 0:
                            time.sleep(timeWait - (tmTmp-tmBegin).seconds)
                        
                        tmBegin = datetime.datetime.now()
                        packageName = get_package_name(packageTmpPath, recordType, nCount, tmBegin)
                        tar = tarfile.open(packageName, 'w:gz') 

                    print('Packing, original file=' + fileName, ', tar file=' + packageName)
                    nFileCount += 1
                    tar.add(fileName, arcname=file)
                    # os.remove(fileName)
                    shutil.move(fileName, bakPath)
                    print("move " + fileName + " from " +  recordPath + " to " + bakPath + "....")
                    
    if not tar.closed:
        tar.close()
        
        nRealCount, nTotalTarFileSize, fileNameList = stat(packageName)
        if nFileCount != nRealCount:
            print("Error: file name is " + packageName, ", Total number of original files =", 
            nFileCount, ", The total number of files in the tar file =", nRealCount, 
            ", Total size of original files =", nTarFileSize, ", Total size of files in the tar file = ",
            nTotalTarFileSize, ", Files: ",  fileNameList) 
        else:
            print("Success: file name is ",  packageName, ", Total number of original files =",
            nFileCount, "The total number of files in the tar file =", nRealCount, 
            "Total size of original files =", nTarFileSize, ", Total size of files in the tar file = ",
            nTotalTarFileSize,", Files: ",  fileNameList)
        
    # 目录中没有文件的情况
    if isDirEmpty:
        os.remove(packageName)
    else:
        shutil.move(packageName, packagePath)

    print("Process " + recordType, " record thread end...\n")        

def main():
    conf = init_config(CONFIG_FILE)
    if -1 == conf:
        print("The config file is not exist!")
        return

    recordTypes = conf.sections()
    print(recordTypes)

    threads = []
    for type in recordTypes: 
        if type != 'COMMON':
            thread = threading.Thread(target=run, args=(conf, type,))
            threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
    
