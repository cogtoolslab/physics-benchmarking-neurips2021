#!/usr/bin/env python
# coding: utf-8

"""NOTE: while this file might be useful to script uploading to S3, use `upload_stims_to_s3.ipynb` for the recent code instead."""

import os
from glob import glob
import boto3
import botocore
from IPython.display import clear_output
import json
import pandas as pd
from PIL import Image
import argparse

def list_files(path, ext='png'):
    result = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.%s' % ext))]
    return result


## helper to speed things up by not uploading images if they already exist, can be overriden 
def check_exists(s3, bucket_name, stim_name):
    try:
        s3.Object(bucket_name,stim_name).load()    
        return True
    except botocore.exceptions.ClientError as e:    
        if (e.response['Error']['Code'] == "404"):
            print('The object does not exist.')
            return False
        else:
            print('Something else has gone wrong with {}'.format(stim_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket_name', type=str, default='human-physics-benchmarking')
    parser.add_argument('--path_to_stim', type=str, default='stimuli')
    parser.add_argument('--overwrite', type=bool, default=False)
    args = parser.parse_args()
    
    ## set up paths, etc.
    bucket_name = args.bucket_name
    path_to_stim = args.path_to_stim
    full_stim_paths = [os.path.abspath(os.path.join(path_to_stim,i)) for i in os.listdir(path_to_stim)]
    print('We have {} images to upload.'.format(len(full_stim_paths)))

    ## tell user some useful information
    print('Path to stimuli is : {}'.format(path_to_stim))
    print('Uploading to this bucket: {}'.format(bucket_name))

    ## establish connection to s3 
    s3 = boto3.resource('s3')

    ## create a bucket with the appropriate bucket name
    try: 
        b = s3.create_bucket(Bucket=bucket_name) 
        print('Created new bucket.')
    except:
        b = s3.Bucket(bucket_name)
        print('Bucket already exists or credentials missing')

    ## do we want to overwrite files on s3?
    overwrite = args.overwrite

    ## set bucket and objects to public
    b.Acl().put(ACL='public-read') ## sets bucket to public

    ## now let's loop through stim paths and actually upload to s3 (woot!)
    for i,path_to_file in enumerate(full_stim_paths):        # use sorted(full_stim_paths) when not using photodraw32
        stim_name = os.path.split(path_to_file)[-1]
        if ((check_exists(s3, bucket_name, stim_name)==False) | (overwrite==True)):
            print('Now uploading {} as {} | {} of {}'.format(os.path.split(path_to_file)[-1],stim_name,(i+1),len(full_stim_paths)))
            s3.Object(bucket_name,stim_name).put(Body=open(path_to_file,'rb')) ## upload stimuli
            s3.Object(bucket_name,stim_name).Acl().put(ACL='public-read') ## set access controls
        else: 
            print('Skipping {} | {} of {} because it already exists.'.format(os.path.split(path_to_file)[-1],(i+1),len(full_stim_paths)))
        clear_output(wait=True)

    print('Done!')
