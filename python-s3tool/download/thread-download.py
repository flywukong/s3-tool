# This program is  a test of S3 multpart upload API
#*-*coding:utf-8 *-*  
import sys
import traceback
import argparse
import threading
import Logger
from boto3.s3.transfer import TransferConfig, S3Transfer
import boto3
from boto3.session import Session
import time 

def timer(func):

    def decor(*args,**kwargs):

        start_time = time.time();
        func(*args);
        end_time = time.time();
        d_time = end_time - start_time
        print "download file  use {} seconds".format(d_time)


class ProgressPercentage2(object):
    def __init__(self,client,bucket,filename):
        self._filename = filename
        self._size = float(client.head_object(Bucket=bucket, Key=filename)['ContentLength'])
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = round((self._seen_so_far / self._size) * 100,2)
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s %s / %s (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size, percentage))

#            sys.stdout.write('{} is the file name. {} out of {} done. The percentage completed is {} %'.format(str(self._filename), str(self._seen_so_far), str(self._size),str(percentage)))
            sys.stdout.flush()

def download_file(s3_client,bucketname,keyname,filepath):

    try:
        print "Downloading file:", filepath
        down_config = TransferConfig(
    		multipart_threshold= 32 * 1024 * 1024,
		max_concurrency=20,
                multipart_chunksize= 16 * 1024 * 1024,
    		num_download_attempts=10,
                max_io_queue=10000
	)
        t = S3Transfer( client=s3_client,config=down_config )
                           
        progress = ProgressPercentage2(s3_client,bucketname,keyname)
       # progress = ProgressPercentage(filepath)
        t.download_file( bucketname, keyname, filepath, callback=progress )

    except Exception as e:
        print "Error downloading: %s" % ( e )



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hostname', help='radosgw hostname', required=True)
    parser.add_argument('-a', '--access-key', help='S3 access key', required=True)
    parser.add_argument('-s', '--secret-key', help='S3 secret key', required=True)
    parser.add_argument('-b', '--bucket',help ='bucket name',required=True)
    parser.add_argument('-o', '--key',help ='object name',required=True)
    parser.add_argument('-f', '--filepath',help ='down load filepath',required=True)

    args = parser.parse_args()

    url = args.hostname
    session = Session(args.access_key,args.secret_key)
    s3_client = session.client('s3', endpoint_url=url)

    filepath = args.filepath+"/"+args.key
    keyname = args.key

    bucketname = args.bucket

    download_file(s3_client,bucketname,keyname,filepath)
      


