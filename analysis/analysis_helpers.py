import numpy as np
from itertools import groupby
import numpy as np
import scipy.stats as stats
import pandas as pd

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
    X = np.random.choice(a=['False', 'True'], size=(1000, numTrials), p=[probResp, 1-probResp])
    Maxx = []
    for x in X:
        lst = []
        for n,c in groupby(x):
            num,count = n,sum(1 for i in c)
            lst.append((num,count))
        maxx = max([y for x,y in lst])
        Maxx.append(maxx)
    return np.percentile(Maxx,97.5)


def get_longest_streak_length(seq):
    lst = []
    for n,c in groupby(seq):
        num,count = n,sum(1 for i in c)
        lst.append((num,count))
    return max([y for x,y in lst])


def apply_exclusion_criteria(D):
    
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
    
    ## print name of scenario
    scenarionName = np.unique(D['scenarioName'])[0]
    
    ## init flaggedIDs var
    flaggedIDs = []    
    
    ## what is 97.5th percentile for random sequences of length numTrials and p=0.5?
    thresh = get_streak_thresh(150, 0.5)
    print('97.5th percentile for streak length is {}.'.format(thresh)) 
    
    ## flag sessions with long streaks
    streakyIDs = []
    for name, group in D.groupby('gameID'):
        seq = group['response'].values
        streak_length = get_longest_streak_length(group['response'].values)
        if streak_length>thresh:
            streakyIDs.append(name)
    print('There are {} flagged IDs so far due to long streaks.'.format(len(streakyIDs)))
    
    ## flag sessions with suspicious alternation pattern
    alternatingIDs = []
    pattern = list(np.unique(D['response'].values))*10
    for name, group in D.groupby('gameID'):
        seq = group['response'].values
        substr = ''.join(pattern)
        fullstr = ''.join(seq)
        if substr in fullstr:
            alternatingIDs.append(name)
    print('There are {} flagged IDs so far due to alternating sequences.'.format(len(alternatingIDs)))
    
    ## TODO: flag familiarization trial failures    
    print('TODO: Still need to flag familiarization trial failures!!!!')
    
    ## flag sessions with unusually low accuracy
    Dacc = D.groupby('gameID').agg({'correct':np.mean})
    thresh = np.mean(Dacc['correct']) - 3*np.std(Dacc['correct'])
    Dacc = Dacc.assign(lowAcc = Dacc['correct']<thresh)
    lowAccIDs = list(Dacc[Dacc['lowAcc']==True].index)
    print('There are {} flagged IDs so far due to low accuracy.'.format(len(lowAccIDs))) 
    
    ## flag sessions with unusually high RTs
    Drt = D.groupby('gameID').agg({'logRT':np.median})
    thresh = np.median(Drt['logRT']) + 3*np.std(Drt['logRT'])
    Drt = Drt.assign(highRT = Drt['logRT']>thresh)
    highRTIDs = list(Drt[Drt['highRT']==True].index)
    print('There are {} flagged IDs so far due to high RTs.'.format(len(highRTIDs)))    
    
    ## combining all flagged sessions
    flaggedIDs = streakyIDs + alternatingIDs + lowAccIDs + highRTIDs
    print('There are a total of {} flagged IDs.'.format(len(np.unique(flaggedIDs))))  
    
    ## removing flagged sessions from dataset
    D = D[~D.gameID.isin(flaggedIDs)]
    numSubs = len(np.unique(D.gameID.values))
    print('There are a total of {} valid and complete sessions for {}.'.format(numSubs, scenarionName))   
    
    return D




