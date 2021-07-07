import os
import boto3
import botocore
import argparse
from glob import glob
import argparse

'''
To download features & metadata, use command: python download_results.py 

'''

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--path_to_data', type=str, help='path to data', default='../results/csv/')
  parser.add_argument('--bucket_name', type=str, help='bucket_name', default='physics-benchmarking-results')
  parser.add_argument('--overwrite', type=str2bool, help='if True, will overwrite local with download from S3',
                      default='False')
  args = parser.parse_args()

  bucket_name = args.bucket_name
  path_to_data = args.path_to_data
  overwrite = args.overwrite
  print('Bucket name: {}'.format(bucket_name))
  print('Data will download to: {}'.format(path_to_data))
  print('Overwrite local data with downloaded data from S3? {}'.format(overwrite))

  ## create data subdirs if they do not exist
  os.makedirs(path_to_data) if not os.path.exists(path_to_data) else None
  if not os.path.exists(os.path.join(path_to_data,'humans')):
    os.makedirs(os.path.join(path_to_data,'humans'))
    os.makedirs(os.path.join(path_to_data,'models'))

  ## establish connection to s3 
  s3 = boto3.resource('s3')  
  b = s3.Bucket(bucket_name)

  print('Initiating download from S3 ...')
  agentList = ['humans', 'models']
  ## get features from each agent
  for agent in agentList:
    r = list(b.objects.filter(Prefix=agent))
    for i, _r in enumerate(r):
      if overwrite==True or os.path.exists(os.path.join(path_to_data,_r.key))==False:
        print('Currently downloading {} | file {} of {}'.format(_r.key, i+1, len(r)))
        s3.meta.client.download_file(bucket_name, _r.key, os.path.join(path_to_data,_r.key))
      else:
        print('Already have {} | file {} of {}'.format(_r.key, i+1, len(r)))