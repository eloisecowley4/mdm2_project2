
import pandas as pd

_data_path = 'data'
_metadata = pd.read_csv(f'{_data_path}/metadata.csv')

def get_experement_paths(group_size:int|None = None,limit:int|None = None) -> list[str] :
    '''
    returns list of file paths leading to experements that match the filter requirements
    group_size : the size of the group of fish used in the experiment (filter defaluts to none)
    limit : the max number of experements you want back
    '''

    valid_paths = []
    
    for row in _metadata.iloc : 
        # check group size
        if (group_size is not None) and (row['FishNb'] != group_size)  :
            continue

        # path is valid
        valid_paths.append(
            f'{_data_path}/{row['FishNb']}/{row['ExpID']}.csv'
            )

        # check limit
        if (limit is not None) and (len(valid_paths) == limit) :
            break

    return valid_paths


def metadata_from_path(path:str) -> pd.DataFrame :
    '''
    returns metadata about an experement given its path
    '''
    _,group_size, experiment = path.replace('.csv', '').split('/')

    # find row relating to this experiment
    for row in _metadata.iloc :
        if (row['FishNb'] == group_size) and (row['ExpID'] == experiment) :
            break
    
    return row 


if __name__ == '__main__' :

    for path in get_experement_paths() :
        print(*metadata_from_path(path))