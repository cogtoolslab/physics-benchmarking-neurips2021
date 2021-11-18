import numpy as np
from itertools import groupby
import numpy as np
import scipy.stats as stats
import pandas as pd

# which columns identify a model?
MODEL_COLS = [
     'Model',
     'Readout Train Data',
     'Readout Type',
     'Encoder Type',
     'Dynamics Type',
     'Encoder Pre-training Task',
     'Encoder Pre-training Dataset',
     'Encoder Pre-training Seed',
     'Encoder Training Task',
     'Encoder Training Dataset',
     'Encoder Training Seed',
     'Dynamics Training Task',
     'Dynamics Training Dataset',
     'Dynamics Training Seed',
     'ModelID',
     'Model Kind']
# Which columns can we abstract over the concrete dataset over?
DATASET_ABSTRACTION_COLS = ['Encoder Training Dataset',
    'Dynamics Training Dataset', 'Readout Train Data']
DATASET_ABSTRACTED_COLS = [c + " Type" for c in DATASET_ABSTRACTION_COLS]


def item(x):
    """Returns representative single item; helper function for pd.agg"""
    return x.tail(1).item()


def get_streak_thresh(numTrials, probResp):
    '''
    input:
        numTrials: how many trials
        probResp: probability of True response
    output:
        prints the 97.5th percentile for unusual streak lengths
    '''
    X = np.random.choice(a=['False', 'True'], size=(
        1000, numTrials), p=[probResp, 1-probResp])
    Maxx = []
    for x in X:
        lst = []
        for n, c in groupby(x):
            num, count = n, sum(1 for i in c)
            lst.append((num, count))
        maxx = max([y for x, y in lst])
        Maxx.append(maxx)
    return np.percentile(Maxx, 97.5)


def get_longest_streak_length(seq):
    lst = []
    for n, c in groupby(seq):
        num, count = n, sum(1 for i in c)
        lst.append((num, count))
    return max([y for x, y in lst])


def bootstrap_mean(D, col='correct', nIter=1000):
    bootmean = []
    for currIter in np.arange(nIter):
        bootD = D.sample(n=len(D), random_state=currIter, replace=True)
        bootmean.append(np.mean(bootD[col].values))
    return bootmean


def load_and_preprocess_data(path_to_data):
    '''
    apply basic preprocessing to human dataframe
    '''

    # load in data
    d = pd.read_csv(path_to_data)

    # add column for scenario name
    scenarioName = path_to_data.split('/')[-1].split('-')[1].split('_')[0]

    # some utility vars
    # colnames_with_variable_entries = [col for col in sorted(d.columns) if len(np.unique(d[col]))>1]
    colnames = ['gameID', 'trialNum', 'prolificIDAnon', 'stim_ID',
        'response', 'target_hit_zone_label', 'correct', 'choices', 'rt']
    # colnames = ['gameID','trialNum','stim_ID','response','target_hit_zone_label','correct','choices','rt']
    # include all the columns that we can
    intersect_cols = [col for col in colnames if col in d.columns]

    # subset dataframe by colnames of interest
    _D = d[intersect_cols]
    _D = _D.assign(scenarioName=scenarioName)

    _D = basic_preprocessing(_D)

    return _D

def basic_preprocessing(_D):
    try:
        # preprocess RTs (subtract 2500ms presentation time, log transform)
        _D = _D.assign(RT=_D['rt'] - 2500)
        _D = _D.assign(logRT=np.log(_D['RT']))
        _D = _D.drop(columns=['rt'], axis=1)
    except:
        _D['RT'] = np.nan
        _D['logRT'] = np.nan

    # convert responses to boolean
    binary_mapper = {'YES': True, 'NO': False, np.nan: np.nan, "Next":np.nan} # Next can show up when we feed in the results of a familiarization dataframe—ignore it for present purposes
    _D = _D.assign(responseBool=_D['response'].apply(
        lambda x: binary_mapper[x]), axis=0)

    # remove _img from stimulus name
    _D['stim_ID'] = _D['stim_ID'].apply(lambda n: n.split("_img")[0])
    return _D


def apply_exclusion_criteria(D, familiarization_D=None, verbose=False):
    '''
     Based on `preregistration_neurips2021.md`

     Data from an entire experimental session will be excluded if the responses:
     * contain a sequence with unusually long streak, defined as occurring less than 2.5% of the time under random responding
     * contain a sequence of at least 24 trials alternating "yes" and "no" responses
     * are correct for fewer than 4 out of 10 familiarization trials (i.e., 30% correct or lower)
     * the mean accuracy for that participant is below 3 standard deviations below the median accuracy across all participants for that scenario
     * the mean log-transformed response time for that participant is 3 standard deviations above the median log-transformed response time across all participants for that scenario

    Excluded sessions will be flagged. Flagged sessions will not be included in the main analyses. We will also conduct our planned analyses with the flagged sessions included to investigate the extent to which the outcomes of the main analyses change when these sessions are included. Specifically, we will fit a statistical model to all sessions and estimate the effect of a session being flagged on accuracy.

    input: D, dataframe from a specific experiment w/ a specific physical domain
    output: D, filtered dataframe after exclusions have been applied
    '''

    # print name of scenario
    scenarionName = np.unique(D['scenarioName'])[0]

    # check if we have prolificIDAnon
    if 'prolificIDAnon' in D.columns:
        userIDcol = 'prolificIDAnon'
    else:
        userIDcol = 'gameID'
        if verbose:
            print("WARNING: no prolificIDAnon column found. Using gameID instead.")

    # init flaggedIDs var
    flaggedIDs = []

    # what is 97.5th percentile for random sequences of length numTrials and p=0.5?
    thresh = get_streak_thresh(150, 0.5)
    if verbose:
        print('97.5th percentile for streak length is {}.'.format(thresh))

    # flag sessions with long streaks
    streakyIDs = []
    for name, group in D.groupby(userIDcol):
        seq = group['response'].values
        streak_length = get_longest_streak_length(group['response'].values)
        if streak_length > thresh:
            streakyIDs.append(name)
    if verbose:
        print('There are {} flagged IDs so far due to long streaks.'.format(
            len(streakyIDs)))

    # flag sessions with suspicious alternation pattern
    alternatingIDs = []
    pattern = list(D['response'].dropna().unique())*10
    for name, group in D.groupby(userIDcol):
        seq = group['response'].dropna().values
        substr = ''.join(pattern)
        fullstr = ''.join(seq)
        if substr in fullstr:
            alternatingIDs.append(name)
    if verbose:
        print('There are {} flagged IDs so far due to alternating sequences.'.format(
            len(alternatingIDs)))

    # flag sessions that failed familiarization
    # see familiarization_exclusion.py
    if familiarization_D is None:
        # is familirization dataframe provided in D?
        try:
            if np.sum(D['condition'] == 'familiarization_prediction') > 0:
                familiarization_D = D[D['condition'] == 'familiarization_prediction']
                if verbose:
                    print('Familiarization dataframe provided in D.')
        except:
                if verbose: print('Familiarization dataframe not provided in D.')
    if familiarization_D is not None:
        # do we have coverage for all prolific IDs?
        if verbose: print('Familiarization dataframe has {} rows.'.format(len(familiarization_D)))
        if set(np.unique(familiarization_D[userIDcol])) != set(np.unique(D[userIDcol])):
            if verbose: print('Not all prolific IDs are covered in familiarization data. Make sure you pass familiarization data for all trials!')
        try:
            C_df = familiarization_D.groupby('gameID').agg({'correct': ['sum', 'count']})
            # get ratio
            C_df['ratio'] = C_df[('correct', 'sum')]/C_df[('correct', 'count')]
            C_df_excluded = C_df[C_df['ratio'] <= .3]
            # get ProlificIDs for excluded sessions
            excludedIDs = C_df_excluded.index.values
            # get ProlificIDs for gameIDs
            famIDs = []
            for gameID in excludedIDs:
                famIDs.append(np.unique(familiarization_D[familiarization_D['gameID'] == gameID][userIDcol])[0])
        except:
            if verbose: print("An error occured during familiarization exclusion")
        if verbose:
            print("There are {} flagged IDs due to failing the familiarization trials".format(len(C_df_excluded)))
    else:
        if verbose: print('No familiarization data provided. Pass a dataframe with data from the familiarization trials (full dataframe is okay). Skipping familiarization exclusion.')
    
    # flag sessions with unusually low accuracy
    # ignore nan responses
    Dacc = D[D['correct'].isna() == False]
    Dacc['correct'] = Dacc['correct'].astype(int)
    Dacc = Dacc.groupby(userIDcol).agg({'correct':'mean'})
    thresh = np.mean(Dacc['correct']) - 3*np.std(Dacc['correct'])
    Dacc = Dacc.assign(lowAcc = Dacc['correct']<thresh)
    lowAccIDs = list(Dacc[Dacc['lowAcc']==True].index)
    if verbose:
        print('There are {} flagged IDs so far due to low accuracy.'.format(len(lowAccIDs))) 
    
    # flag sessions with unusually high RTs
    Drt = D.groupby(userIDcol).agg({'logRT':np.median})
    thresh = np.median(Drt['logRT']) + 3*np.std(Drt['logRT'])
    Drt = Drt.assign(highRT = Drt['logRT']>thresh)
    highRTIDs = list(Drt[Drt['highRT']==True].index)
    if verbose:
        print('There are {} flagged IDs so far due to high RTs.'.format(len(highRTIDs)))    
    
    # combining all flagged sessions
    flaggedIDs = streakyIDs + alternatingIDs + lowAccIDs + highRTIDs
    if verbose:
        print('There are a total of {} flagged IDs.'.format(len(np.unique(flaggedIDs))))  

    # we also need to exclude ledge stimuli until their reprodicibility is fixed
    mask = ~D['stim_ID'].str.contains("ledge")
    D = D[mask]
    if verbose:
        print("{} observations are excluded due to removal of ledge stimuli".format(np.sum(~mask)))

    # removing flagged sessions from dataset
    D = D[~D[userIDcol].isin(flaggedIDs)]
    numSubs = len(np.unique(D[userIDcol].values))
    if verbose:
        print('There are a total of {} valid and complete sessions for {}.'.format(numSubs, scenarionName))   
    
    return D

def same_or_nan(acol,bcol): return [a if a != b else np.nan for a,b in zip(acol,bcol)]

def process_model_dataframe(MD):
    """Apply a couple of steps to read in the output of the model results"""

    # add correctness info
    MD['correct'] = MD['Actual Outcome'] == MD['Predicted Outcome']

    # reverse renaming of scenarios
    MD = MD.replace('rollslide','rollingsliding')
    MD = MD.replace('cloth','clothiness')
    MD = MD.replace('no_rollslide','no_rollingsliding')
    MD = MD.replace('no_cloth','no_clothiness')

    # add canonical stim name (ie remove redyellow)
    MD['Canon Stimulus Name'] = MD['Stimulus Name'].apply(lambda n: "".join(n.split('-redyellow')))

    # set dataset columns to 'same' if they match the test data
    for col in DATASET_ABSTRACTION_COLS:
        MD[col+" Type"] = MD[col]
        MD.loc[MD[col] == MD["Readout Test Data"],col+" Type"] = "same"
        MD.loc[MD[col] == ["no_"+n for n in MD["Readout Test Data"]],col+" Type"] = "all_but_this"
        # MD.loc[MD[col] == "all",col+" Type"] == "all

    # force unique model string
    MD['ModelID'] = ["_".join(attr) for attr in zip(
    MD['Model'].astype(str),
    MD['Encoder Type'].astype(str),
    MD['Encoder Training Seed'].astype(str),
    MD['Encoder Training Task'].astype(str), 
    MD['Encoder Training Dataset'].astype(str),
    MD['Dynamics Training Task'].astype(str),
    MD['Dynamics Training Seed'].astype(str),
    MD['Dynamics Training Dataset'].astype(str),
    ["readout"]*len(MD),
    MD['Readout Type'].astype(str),
    MD['Readout Train Data'].astype(str),
    MD['filename'].astype(str)
    )]
    
    # force unique model string
    MD['ModelID'] = ["_".join(attr) for attr in zip(
    MD['Model'].astype(str),
    MD['Encoder Type'].astype(str),
    MD['Encoder Training Seed'].astype(str),
    MD['Encoder Training Task'].astype(str), 
    MD['Encoder Training Dataset'].astype(str),
    MD['Dynamics Training Task'].astype(str),
    MD['Dynamics Training Seed'].astype(str),
    MD['Dynamics Training Dataset'].astype(str),
    ["readout"]*len(MD),
    MD['Readout Type'].astype(str),
    MD['Readout Train Data'].astype(str),
    MD['filename'].astype(str)
    )]

    # add a model kind—the granularity that we want to plot over—columns
    # this ignores the specific datasets if they match the testing data, but not otherwise
    # ignores Dynamics Training, so we can loop over it in plotting
    # get a list of models to plot
    MD['Model Kind'] = ["_".join(attr) for attr in zip(
        MD['Model'].astype(str),
        MD['Encoder Type'].astype(str),
        MD['Encoder Training Seed'].astype(str),
        MD['Encoder Training Task'].astype(str), 
        MD['Encoder Training Dataset Type'].astype(str),
        MD['Dynamics Training Task'].astype(str),
        MD['Dynamics Training Seed'].astype(str),
        # MD['Dynamics Training Dataset Type'].astype(str),
        MD['Readout Train Data Type'].astype(str),
    )]

    return MD
