Lecheval, V. et al. (2018). Social conformity and propagation of information in 
collective U-turns of fish schools.

The data consist in experimental 2D-trajectories of schools of fish swimming 
freely in a ring-shaped tank (inner wall: radius of 25cm; outer wall: 35cm; 
water-level: 7cm) during approximately 60 minutes. There are 68 experiments 
included in this dataset. Individual trajectories of fish swimming alone or
fish in groups of 2, 4, 5, 8 or 10 individuals are recorded at 50 frames per 
second (more details in the Material and Methods section of the article).
Data of experiments with 20 fish have not been tracked automatically (i.e.
trajectories are not available): times of collective and individual U-turns
have been recorded by eye and are included.

The dataset contains:

- metadata.txt, a data frame that contains the metadata of the 58 experiments 
  conducted. Each row is a different experiment.
  Variables are:
    FishNb: group size
    ExpID: label of the experiment written as exp01H20141128_14h10 where '01'
	       is the group size, 'H' the size of the outer wall of the 
		   ring-shaped tank (35cm, inner wall: 25cm) and 20141128_14h10 is 
		   date_time.
    ExpLength: the duration of the experiment (in minutes)
    Fps: the frame rate, in frame per seconds
    BLi: the body length (in mm) of individual i in the current experiment
	
- 6 zip files (1.zip, 2.zip, 4.zip, 5.zip, 8.zip, 10.zip). Each archive 
  contains the data of each experiment for the respective group size (i.e. 
  1.zip contains data of experiments with 1 fish). There is one csv file per 
  experiment. Each csv file contains the position (X, Y, in mm) and heading (H,
  in radians) of each fish, for each frame of the experiment (rows). The 
  column 'X2' stands for the x-coordinates of the fish #2 and H4 for the 
  headings of the fish #4.
  
- 1 zip file 20.zip which contains datasets for groups of 20 fish (11 
  experiments). Two files are included :
    - durations_coll_turns.csv with the first frame and last frame of 
	each collective U-turn. Column ExpID gives the experiment. NA (non
	available) refers to experiments without collective U-turn.
	- time_indiv_turns.csv gives the frame at which each individual turns
	for	each collective U-turn. Columns refer to collective U-turn, one
	Row per individual.

