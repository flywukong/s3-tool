#!/usr/bin/python

import os
import sys
import boto
import argparse
import threading
import Logger
import boto.s3.connection
from boto.s3.key import Key


LOG = Logger.getLogger("s3.log")

from boto3.s3.transfer import TransferConfig, S3Transfer
import boto3
from boto3.session import Session


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s %s / %s (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size, percentage))
            sys.stdout.flush()


def thread_upload_file( s3client, filename, bucketname, keyname):

    try:
        print "Uploading file:", filename
        upload_config = TransferConfig(
                multipart_threshold= 32 * 1024 * 1024,
                max_concurrency= 20,
                multipart_chunksize= 16 * 1024 * 1024,
        )

        t = boto3.s3.transfer.S3Transfer( client=s3client,
                                         config=upload_config )

        t.upload_file(filename, bucketname, keyname, callback=ProgressPercentage(filename))

    except Exception as e:
        print "Error uploading: %s" % ( e )


# get an access token, local (from) directory, and S3 (to) directory
# from the command-line

def upload_dir(client,bucket,local_directory,destination):


	# enumerate local files recursively
    for root, dirs, files in os.walk(local_directory):

        threads = []
        print "files",files
        for filename in files:
	    # construct the full local path
	    local_path = os.path.join(root, filename)
	    # construct the full s3 path
	    relative_path = os.path.relpath(local_path, local_directory)
	    s3_path = os.path.join(destination, relative_path)

	    # relative_path = os.path.relpath(os.path.join(root, filename))
            print "s3_path",s3_path
            t=threading.Thread(target = thread_upload_file ,args=(client,local_path,bucket,s3_path,))
            threads.append(t)
        for thr in threads:
            thr.start()
        for thr in threads:
            if thr.isAlive():
                thr.join()
         
 

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hostname', help='radosgw hostname', required=True)
    parser.add_argument('-a', '--access-key', help='S3 access key', required=True)
    parser.add_argument('-s', '--secret-key', help='S3 secret key', required=True)
    parser.add_argument('-b', '--bucket',help ='bucket name',required=True)
    parser.add_argument('-l', '--local',help ='local path',required=True)
    parser.add_argument('-d', '--s3path',help ='s3 path',required=True)
    parser.add_argument('-t', '--threadcnt',help ='thread numeber',required=False)
 
    args = parser.parse_args()
    
    url = args.hostname
    session = Session(args.access_key,args.secret_key)
    client = session.client('s3', endpoint_url=url)

    bucketname = args.bucket   
    local_path = args.local
    
    if args.s3path == "root":
        destination = args.local.split("/")[-1]
    else:
    	destination = args.s3path+"/"+args.local.split("/")[-2]
    if args.threadcnt:
        threadcnt = args.threadcnt
    else:
        threadcnt = 20
 
    print "destination",destination
    upload_dir(client,bucketname,local_path,destination)
