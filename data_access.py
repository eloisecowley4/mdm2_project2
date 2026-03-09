
import pandas as pd
import numpy as np

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


def split_at_nans(data:pd.DataFrame) -> list[pd.DataFrame] :
    '''splits data up into chunks whenever there is a block of nan values'''

    # bool mask of if there is a nan value on each row
    na_mask : pd.DataFrame = data.isna()
    na_mask = np.sum(na_mask,axis=1)
    na_mask = na_mask.astype(bool)

    def block_search(data:pd.DataFrame,indexes:slice) -> list[slice] :
        '''finds blocks of True in dataframe using binary search'''
        start, stop = indexes.start, indexes.stop

        # base case
        if start+1 == stop :
            return [indexes] if data.iloc[start] else []

        mid = start + (stop-start)//2
        left, right = slice(start,mid,1), slice(mid,stop,1)

        # left side
        left_datum = na_mask.iloc[left.start]
        if left_datum :
            homogenous = np.all(na_mask.iloc[left])
        else :
            homogenous = np.all(~na_mask.iloc[left])

        if homogenous :
            left_blocks = [left] if left_datum else []
        else :
            left_blocks = block_search(data,left)

        # right side
        right_datum = na_mask.iloc[right.start]
        if right_datum :
            homogenous = np.all(na_mask.iloc[right])
        else :
            homogenous = np.all(~na_mask.iloc[right])
        
        if homogenous :
            right_blocks = [right] if right_datum else []
        else :
            right_blocks = block_search(data,right)

        # combine blocks
        if left_blocks == [] :
            return right_blocks
        elif right_blocks == [] :
            return left_blocks
        
        if left_blocks[-1].stop == right_blocks[0].start :
            # combine slices
            left_slice = left_blocks.pop(-1)
            right_slice = right_blocks.pop(0)
            left_blocks.append(slice(left_slice.start,right_slice.stop))

        return left_blocks + right_blocks
    
    nan_blocks = block_search(data,slice(0,data.shape[0]))

    data_blocks : list[slice] = []

    # convert nan_blocks to data blocks by genorating inverse slices
    temp = sum([[s.start,s.stop] for s in nan_blocks],start=[])
    temp.insert(0,0)
    temp.append(data.shape[0])
    
    for i in range(0,len(temp),2) :
        s = slice(temp[i],temp[i+1],1)
        data_blocks.append(data.iloc[s,:])

    return data_blocks

if __name__ == '__main__' :


    data_path = get_experement_paths(2,1)[0]

    data = pd.read_csv(data_path)
    clean_data = split_at_nans(data)
    print(clean_data)
