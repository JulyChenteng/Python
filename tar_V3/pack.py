import configparser
import os
import tarfile
import time
import datetime
import threading

CONFIG_FILE = "pack.cfg"

def init_config(fileName):
    if os.path.exists( os.path.join(os.getcwd(),fileName) ):
        conf = configparser.ConfigParser()
        conf.read(fileName)
        return conf
    
    return -1

def read_common_options(conf):
    maxSerialNo = conf.getint("COMMON", "MAX_SERIAL_NO")
    maxTarFileSize = conf.getint("COMMON", "MAX_TARFILE_SIZE")
    timeWait = conf.getint("COMMON", "TIME_WAIT")

    return maxSerialNo, maxTarFileSize, timeWait

def get_package_name(packagePath, recordType, nCount, tmBegin ):
    pattern =  '{0:04d}'
    serialNo = pattern.format(nCount)
    strTmBegin = tmBegin.strftime("%Y%m%d%H%M%S")    
    packageName = packagePath + "/" + recordType + "_" + serialNo + "_" + strTmBegin + ".tar"
    
    return packageName

def run(conf, recordType):
    print("Process ", recordType, "record thread begin...")

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
    for _, _, fileList in os.walk(recordPath):
        tmBegin = datetime.datetime.now()
        packageName = get_package_name(packagePath, recordType, nCount, tmBegin)
        tar = tarfile.open(packageName, 'w:gz')

        for fileName in fileList:
            if os.path.isfile(fileName):
                if nCount > maxSerialNo:
                    nCount %= maxSerialNo + 1

                tmTmp = datetime.datetime.now() 
                nTarFileSize += os.path.getsize(fileName)
            
                if nTarFileSize > maxTarFileSize or (tmTmp-tmBegin).seconds >= timeWait:
                    tar.close()
                    
                    nCount += 1
                    nTarFileSize = os.path.getsize(fileName)

                    if timeWait - (tmTmp-tmBegin).seconds > 0:
                        time.sleep(timeWait - (tmTmp-tmBegin).seconds)
                    
                    tmBegin = datetime.datetime.now()
                    packageName = get_package_name(packagePath, recordType, nCount, tmBegin)
                    tar = tarfile.open(packageName, 'w:gz') 
                tar.add(fileName)
                
        if not tar.closed:
            tar.close()
        os.chdir(currPath)

    print("Process ", recordType, "record thread end...\n")        

def main():
    conf = init_config(CONFIG_FILE)
    if -1 == conf:
        print("The config file is not exist!")
        return

    recordTypes = ["GPRS", "GSM", "SMS"]
    threads = []

    for type in recordTypes:
        thread = threading.Thread(target=run, args=(conf, type,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
    
