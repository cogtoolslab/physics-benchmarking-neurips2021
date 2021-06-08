import os, sys
import boto3
import botocore
import argparse
from glob import glob
from tqdm import tqdm
import pandas as pd
import time

'''
To download mp4s and cueing maps, call: 

python download_stimuli.py 

#######

To download hdf5s, call:

python download_stimuli.py --hdf5s
'''

SCENARIOS = ['dominoes', 'support', 'collide', 'contain',
             'drop', 'link', 'roll', 'drape']

OLD_TO_NEW_SCENARIO_NAMES = {
    'dominoes': 'dominoes',
    'towers': 'support',
    'collision': 'collide',
    'containment': 'contain',
    'drop': 'drop',
    'linking': 'link',
    'rollingsliding': 'roll',
    'cloth': 'drape'
}

NEW_TO_OLD_SCENARIO_NAMES = {
    v:k for k,v in OLD_TO_NEW_SCENARIO_NAMES.items()}

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_data',
                        type=str,
                        help='path to downloaded stimulus data',
                        default='./Physion')
    parser.add_argument('--scenarios',
                        type=str,
                        default=','.join(SCENARIOS),
                        help='comma-separated list of scenarios to download')
    parser.add_argument('--hdf5s',
                        action='store_true',
                        help='If passed, download hdf5s rather than mp4s/cues')
    parser.add_argument('--redyellow',
                        action='store_true',
                        help='If passed, download the stimuli with red/yellow objects')
    parser.add_argument('--directory_per_template',
                        action='store_true',
                        help='If passed, each scenario-template gets its own directory.')
    parser.add_argument('--overwrite',
                        action='store_true',
                        help='If passed, overwrite local stimuli')

    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = get_args()
    save_path = args.path_to_data
    overwrite = args.overwrite
    d_per_t = args.directory_per_template
    stim_names = pd.read_csv('./stimuli/stimulus_names_and_labels.csv')[['stim_ID','scenario']]    

    scenarios = [s.lower() for s in args.scenarios.split(',')]
    for sc in scenarios:
        start = time.time()
        assert sc in SCENARIOS, "%s is not one of the scenarios: %s" % (sc, SCENARIOS)
        bsuffix = '' if not (sc == 'drape') else ('sagging' if args.redyellow else 'iness')
        bucket_name = 'human-physics-benchmarking-%s-pilot' % \
            (NEW_TO_OLD_SCENARIO_NAMES[sc] + bsuffix + ('-redyellow' if args.redyellow else ''))
        scenario_path = os.path.join(save_path, sc.capitalize())        
        
        print('Downloading Scenario: {}'.format(sc.capitalize()))
        print('Data will download to: {}'.format(scenario_path))
        print('Overwrite local data with downloaded data from S3? {}'.format(overwrite))

        # create dir where this scenario will be stored
        os.makedirs(scenario_path) if not os.path.exists(scenario_path) else None
        
        # establish connection to s3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)

        ## get stims for this scenario
        r = list(bucket.objects.filter(Prefix=('pilot' if not sc == 'drape' else 'test')))
        suffix = ['mp4', 'png'] if not args.hdf5s else ['hdf5']

        stims = [stim for stim in r if any((s in str(stim) for s in suffix))]
        if not args.redyellow:
            stims = [s for s in stims if 'redyellow' not in s.key]
        else:
            stims = [s for s in stims if 'redyellow' in s.key]

        # keep only the ones that have response data
        sc_names = list(stim_names[stim_names['scenario'] == sc]['stim_ID'])
        print("stims: %s", len(stims))
        print("names: %s", len(sc_names))
        if not args.hdf5s:
            sc_names = [nm + '_img' for nm in sc_names] + ([nm + '_map' for nm in sc_names] if not args.redyellow else [])

        if not args.redyellow:
            stims = [s for s in stims if s.key.split('.')[0] in sc_names]
        else:
            stims = [s for s in stims if ''.join(s.key.split('.')[0].split('-redyellow')) in sc_names]

        # make the savedir if it doesn't exist and save it
        for i,s in enumerate(tqdm(stims)):
            template_name = s.key.split('_0')
            if len(template_name) > 2:
                template_name = '_0'.join(template_name[:-1])
            else:
                template_name = template_name[0]
                
            sv_dir = scenario_path if not d_per_t else os.path.join(scenario_path, template_name)
            sv_type = s.key.split('.')[-1]
            sv_type = 'maps' if sv_type == 'png' else (sv_type + 's')
            if args.redyellow:
                sv_type += '-redyellow'
            sv_dir = os.path.join(sv_dir, sv_type)
            os.makedirs(sv_dir) if not os.path.exists(sv_dir) else None
            s3.meta.client.download_file(bucket_name, s.key, os.path.join(sv_dir, s.key))
        end = time.time()
        print("Successfully downloaded the %s scenario: took %d seconds" % (sc.capitalize(), int(end - start)))
