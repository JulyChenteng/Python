import tarfile
import os

dir_in = "./test/test"
dir_out = "./packages"

def main():
    tar = tarfile.open(dir_out + "/test.tar", 'w:gz')
    for root, _, files in os.walk(dir_in):
        print(root)
        for file in files:
            fullpath = os.path.join(root, file)
            print(file)
            if os.path.isfile(fullpath):
                tar.add(fullpath)
    tar.close()

if __name__ == "__main__":
    main()