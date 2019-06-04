import configparser
import os
import tarfile
import datetime

CONFIG_FILE = "pack.cfg"

def readConfig(fileName):
    if os.path.exists( os.path.join(os.getcwd(),fileName) ):
        conf = configparser.ConfigParser()
        conf.read(fileName)
        return conf
    
    return -1

def getPackageName(packagePath, recordType, nCount, tmBegin):
    if nCount > MAX_SERIAL_NO:
        nCount %= MAX_SERIAL_NO + 1

    pattern =  '{0:04d}'
    serialNo = pattern.format(nCount)
    strTmBegin = tmBegin.strftime("%Y%m%d%H%M%S")    
    packageName = packagePath + "/" + recordType + "_" + serialNo + "_" + strTmBegin + ".tar"
    
    return packageName


def run(recordType, recordPath, maxTarFileSize, packagePath):
    print("Process ", recordType, "record begin...")

    if not os.path.exists(packagePath):
        os.mkdir(packagePath)

    if not os.path.exists(recordPath):
        print("The record path is not exist!\n")
        return

    currPath = os.getcwd()
    recordPath = os.path.join(currPath, recordPath)
    packagePath = os.path.join(currPath, packagePath)
    print(recordPath, " ", packagePath)
    
    os.chdir(recordPath)
    nCount = 0
    nTarFileSize = 0
    for _, _, fileList in os.walk(recordPath):
        for fileName in fileList:
            if os.path.isfile(fileName):
                if 0 == nCount and 0 == nTarFileSize:
                    tmBegin = datetime.datetime.now()
                    packageName = getPackageName(packagePath, recordType, nCount, tmBegin)
                    tar = tarfile.open(packageName, 'w:gz')

                tmTmp = datetime.datetime.now() 
                if (tmTmp-tmBegin).seconds < TIME_WAIT:
                    nTarFileSize += os.path.getsize(fileName)
            
                if nTarFileSize > maxTarFileSize or (tmTmp-tmBegin).seconds >= TIME_WAIT:
                    tar.close()
                    nCount += 1
                    nTarFileSize = 0

                    print(nCount)
                    tmBegin = datetime.datetime.now()
                    packageName = getPackageName(packagePath, recordType, nCount, tmBegin)
                    tar = tarfile.open(packageName, 'w:gz') 
                tar.add(fileName)
                
    if not tar.closed: 
        tar.close()
    os.chdir(currPath)
    print("Process ", recordType, "record end...\n")        

def main():
    conf = readConfig(CONFIG_FILE)
    if -1 == conf:
        print("The config file is not exist!")
        return

    recordType = conf.get("PACK", "RECORD_TYPE")
    maxTarFileSize = conf.getint("PACK", "MAX_TARFILE_SIZE")
    recordPath = conf.get("PACK", "RECORD_PATH") 
    packagePath = conf.get("PACK", "PACKAGE_PATH")

    print(recordPath, recordType, maxTarFileSize, packagePath)

    run(recordType, recordPath, maxTarFileSize, packagePath)
    

if __name__ == "__main__":
    main()
    
