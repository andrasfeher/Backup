#! /usr/bin/python3

import sys
import os
import glob
import hashlib
import json
import urllib

DIGEST_STORE_DIRECTORY = '/home/andras/.directory_digest_store'

def hashFile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)

    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)

    return hasher.digest()

# creates a digest of file digests in a directory
def hashDirectory(startDirectory, directoryHasher):
    fileHasher = hashlib.md5()

    for root, dirnames, filenames in os.walk(startDirectory):
        for filename in filenames:
            # supress all exceptions in connection with file openings and readings
            try:
                directoryHasher.update(hashFile(open(root + '/' + filename, 'rb'), fileHasher))
            except:
                pass

    return directoryHasher.hexdigest()

def encodeDirectoryName(directoryName):
    return directoryName.replace('/', '_')

def getStoredDirectoryDigestPath(directoryName, digest):
    return DIGEST_STORE_DIRECTORY + '/' + directoryName.replace('/', '_').replace('.', '%2') + '.' + digest

def isDirectoryDigestChanged(directoryName, digest):
    return not os.path.exists(getStoredDirectoryDigestPath(directoryName, digest))

def save(directoryName, digest):
    directoryDigestPath = getStoredDirectoryDigestPath(directoryName, digest)

    if not (os.path.exists(DIGEST_STORE_DIRECTORY)):
        os.mkdir(DIGEST_STORE_DIRECTORY)
    else:
        for i in glob.glob(DIGEST_STORE_DIRECTORY + '/' + encodeDirectoryName(directoryName) + '.*'):
            os.unlink(i)

    with open(directoryDigestPath, 'a'):
        os.utime(directoryDigestPath, None)

if __name__ == "__main__":

    digest = hashDirectory(sys.argv[1], hashlib.md5())

    if (isDirectoryDigestChanged(sys.argv[1], digest)):
        print('1') # different
    else:
        print('0') # same

    save(sys.argv[1], digest)
