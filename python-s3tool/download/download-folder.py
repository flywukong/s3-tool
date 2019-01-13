import os
import argparse
from boto3.session import Session
import Logger
import traceback
import threading
from boto3.s3.transfer import TransferConfig, S3Transfer
import boto3
from boto3.session import Session
import sys


LOG = Logger.getLogger("s3.log")
class ProgressPercentage(object):
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

            sys.stdout.flush()


def download_file(s3_client,bucketname,keyname,filepath):

    try:
        filepath = filepath + os.sep + keyname
        print "Downloading file:", filepath
        down_config = TransferConfig(
                multipart_threshold= 32 * 1024 * 1024,
                max_concurrency=10,
                multipart_chunksize= 16 * 1024 * 1024,
                num_download_attempts=10,
                max_io_queue=10000
        )
        t = S3Transfer( client=s3_client,config=down_config )

 #       t = S3Transfer(s3_client)
        progress = ProgressPercentage(s3_client,bucketname,keyname)
        t.download_file( bucketname, keyname, filepath, callback=progress )
#        t.download_file( bucketname, keyname, filepath)
    except Exception as e:
        LOG.error("Error downloading: %s" % ( e ))

   
def download_dir(client, resource, dist, local, bucket):

 
    paginator = client.get_paginator('list_objects')
    from botocore.exceptions import PaginationError
    try:
        page_iterator = paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist)
    except  PaginationError as e:
        LOG.error("bucket {0} paginator get error {1}".format(bucketname,e.response['Error']['Code']))

    for result in page_iterator:
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_dir(client, resource, subdir.get('Prefix'), local, bucket)
    
        if result.get('Contents') is not None:

            threads = []
            for file in result.get('Contents'):
                if not os.path.exists(os.path.dirname(local + os.sep + file.get('Key'))):
                     
                     os.makedirs(os.path.dirname(local + os.sep + file.get('Key')))
                
                keyname = file.get('Key')
                t=threading.Thread(target = download_file,args=(client,bucket,keyname,local,))
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
    parser.add_argument('-b', '--bucketname',help ='bucket name',required=True)
    parser.add_argument('-f', '--filepath',help ='path name',required=True)
    parser.add_argument('-p', '--prefix',help ='prefix name',required=True)

    args = parser.parse_args()

    url = args.hostname
    session = Session(args.access_key,args.secret_key)
    client = session.client('s3', endpoint_url=url)

    resource = boto3.resource('s3', endpoint_url=url, aws_access_key_id = args.access_key, aws_secret_access_key=args.secret_key)
    
    file_path = args.filepath
    prefix = args.prefix+"/"
    bucketname = args.bucketname

    download_dir(client, resource, prefix, file_path,bucketname)

