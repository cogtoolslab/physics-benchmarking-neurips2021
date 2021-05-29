import os
import boto3
import botocore
import argparse
from glob import glob
import argparse

'''
To upload results, run:
python upload_results.py --path_to_data=../results/csv/ --bucket_name=physics-benchmarking-results

'''

def check_exists(s3, bucket_name, filename):
    '''
    helper to speed things up by not uploading images if they already exist, can be overriden 
    '''
    try:
        s3.Object(bucket_name,filename).load()    
        return True
    except botocore.exceptions.ClientError as e:    
        if (e.response['Error']['Code'] == "404"):
            print('The object does not exist.')
            return False
        else:
            print('Something else has gone wrong with {}'.format(filename))

def list_files(path, ext = 'npy'):
    return [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.{}'.format(ext) ))]

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1", "True", "TRUE")        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--path_to_data', type=str, help='path to data', default='../results/csv/')
    parser.add_argument('--bucket_name', type=str, help='bucket_name', default='physics-benchmarking-results')
    parser.add_argument('--overwrite', type=str2bool, help='boolean flag to set to overwrite what is in S3 or not', default='False')
    parser.add_argument('--public_read', type=str2bool, help='boolean flag to set to publicly readable or not', default='False')
    args = parser.parse_args()
    
    ## get list of paths to datafiles
    csv_paths = list_files(args.path_to_data,ext='csv')
    data_paths = csv_paths

    ## tell user some useful information
    print('Path to data is : {}'.format(args.path_to_data))
    print('Uploading to this bucket: {}'.format(args.bucket_name))
    print('Set ACL settings to public-read: {}'.format(args.public_read))

    ## establish connection to s3 
    s3 = boto3.resource('s3')

    ## create a bucket with the appropriate bucket name
    try: 
        b = s3.create_bucket(Bucket=args.bucket_name) 
        print('Created new bucket.')
    except:
        b = s3.Bucket(args.bucket_name)
        print('Bucket already exists.')

    ## set bucket and objects to public
    if args.public_read==True:
        b.Acl().put(ACL='public-read') ## sets bucket to public

    ## now let's loop through data paths and actually upload to s3 
    for i, path_to_file in enumerate(data_paths):
        filename = path_to_file.split('/')[-1]
        dirname = path_to_file.split('/')[-2]
        keyname = os.path.join(dirname,filename)

        if ((check_exists(s3, args.bucket_name, keyname)==False) | (args.overwrite==True)):
            print('Now uploading {} | {} of {}'.format(path_to_file.split('/')[-1],(i+1),len(data_paths)))
            s3.Object(args.bucket_name,keyname).upload_file(path_to_file) ## upload data
            if args.public_read==True:
                s3.Object(args.bucket_name,keyname).Acl().put(ACL='public-read') ## set access controls
        else: 
            print('Skipping {} | {} of {} because it already exists.'.format(path_to_file.split('/')[-1],(i+1),len(data_paths)))