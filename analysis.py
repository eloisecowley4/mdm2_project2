import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
import numpy as np


def find_significant_events(experement:pd.DataFrame, window_size:int = 150, turn_threshold:float = np.pi):
    '''
    Calculates a windowed differance for the angle of turn. 
    Filters arrays of the signifiacnt turn events defined by a turn threshold.

    Parameters:
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

def find_peaks_from_significant_events(significant_events:pd.DataFrame, turn_threshold:float = np.pi, window_size:int = 150):
    '''
    Identifies the indeces of local maximums (peaks) for each heading differance column.
        The function processes each column independantly to find peaks that exceed a specific maximum.
        It uses a window size to ensure that a noisy function are not counted multipul turns.  

    significant_events: pd.DataFrame
        DataFrame containing the filtered rows for stustained turn over a value. 
        Each cloumn represets one fish
    window_size: int, optional
        The number of frames over which to calculate the turn (default is 150).
    turn_threshold: float, optional
        The radian value a turn must exceed to be 'significant' (default is pi).

    Returns:pd.DataFrame
        A long-format DataFrame with two columns:
        - 'column_name': The original signal source (e.g., 'H1', 'H2').
        - 'peak_index': The integer position of the identified peak.
    '''
    all_peaks = (
    significant_events
    .apply(lambda x: find_peaks(x.abs().fillna(0), height=turn_threshold, distance=window_size)[0])
    .explode()
    .reset_index()
    )
    all_peaks.columns = ['column_name', 'peak_index']

    return all_peaks

    
