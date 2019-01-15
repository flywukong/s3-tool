# -*- coding: utf-8 -*- 
import Logger
import traceback

import boto
from boto3.session import Session
import boto3
import argparse
import threading


LOG = Logger.getLogger("s3.log")

def del_objects(bucket,objects):

    for i in range(3):
        try:    
            bucket.delete_objects(
                Delete={'Objects': objects}
            )
            break
        except Exception as err:
            LOG.error("deleting list {0} err".format(objects))
            LOG.error(traceback.format_exc())
            LOG.error(err)
   
def del_bucket(s3,client,bucketname):


    print "deleting",bucketname
   
# Create a reusable Paginator
    paginator = client.get_paginator('list_objects')

# Create a PageIterator from the Paginator
    from botocore.exceptions import PaginationError
    try:
        page_iterator = paginator.paginate(Bucket=bucketname)
    except  PaginationError as e:
        LOG.error("bucket {0} paginator get error {1}".format(bucketname,e.response['Error']['Code']))
  
    threads = []

    for page in page_iterator:
   
         object_to_delete = []
     
         if 'Contents' in page.keys():
             for obj in page['Contents']:
     	         object_to_delete.append({'Key':obj['Key']})

         bucket = s3.Bucket(bucketname)

         t=threading.Thread(target = del_objects,args=(bucket,object_to_delete,))
         threads.append(t)
	    
    for thr in threads:
        thr.start()
    for thr in threads:
    	if thr.isAlive():
            thr.join()

   
    from botocore.exceptions import ClientError
    try:
        resp = s3_client.delete_bucket(Bucket=bucketname)
    except ClientError as e:
	LOG.error("delete bucket {0} error {1}".format(bucketname,e.response['Error']['Code']))



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hostname', help='radosgw hostname', required=True)
    parser.add_argument('-a', '--access-key', help='S3 access key', required=True)
    parser.add_argument('-s', '--secret-key', help='S3 secret key', required=True)
    parser.add_argument('-f', '--filepath',help ='file path',required=True)
    args = parser.parse_args()

    url = args.hostname
    session = Session(args.access_key,args.secret_key)
    s3_client = session.client('s3', endpoint_url=url)
  
    s3 = boto3.resource('s3', endpoint_url=url, aws_access_key_id = args.access_key, aws_secret_access_key=args.secret_key)

    file_name = args.filepath
   
    bucket_list = [] 
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if  line.strip():
                bucket_list.append(line.strip())
 
    threads = [] 
    for bucketname in bucket_list:

        t=threading.Thread(target = del_bucket,args=(s3,s3_client,bucketname,))
        threads.append(t)
    for thr in threads:
        thr.start()
    for thr in threads:
        if thr.isAlive():
            thr.join()
