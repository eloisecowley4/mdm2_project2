import matplotlib.pyplot as plt
import pandas as pd

def find_significant_events(experement:pd.DataFrame, window_size:int = 150, turn_threshold:float = np.pi):
    '''
    Filters arrays of the signifiacnt turn events and the angle (rad) of turn over the window. 

    experement : pd.DataFrame
        The raw data incluing column headings. 
    window_size : int, optional
        The number of frames over which to calculate the turn (default is 150).
    turn_threshold : float, optional
        The radian value a turn must exceed to be 'significant' (default is pi).

    Retruns:
    pd.DataFrame
        A dataframe of sustained turn values, keeping only the 'significant' rows.
        The original frame indices from the input are preserved.
    '''
    headings = experement.iloc[:,2::3]
 
    sustained_turn = headings.diff(periods=window_size)

    filter = (sustained_turn.abs() > turn_threshold).any(axis=1)

    return sustained_turn[filter]
