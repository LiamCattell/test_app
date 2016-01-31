import pandas as pd
    
###############################################################################
# JOBS DATA
###############################################################################
def load_jobs(profession_key, name_root='data/jobsdata'):
    """
    Load jobs data from a pickle file
    """
    return pd.read_pickle(name_root + '_' + profession_key)