For runnning code.

The PulP ILP model is within the firefighter.py script and
the MiniZinc CSP model is implemented in the firefighter.mzn script.

The firefighter.py script also functions as the experimental pipeline,
when passed a folder containing a set of benchmark instances following
the correct format it will execute each solver on each instance and
output a csv file of the format times_[n]nodes_[FOLDER_NAME].csv.

For example python3 firefighter.py BBGRLTestSet/ will output
times_[n]nodes_BBGRLTestSet.csv where the first line is the PulP
times separated by commas and the second line is the mzn times.

The plotTimes.py file will plot the times for each csv file given as command
line inputs, multiple csv files can be given and each one will be plot with
a different colour with the appropriate label in the plot's legend.

The number of nodes n is set in the firefighter.py file on line 11 and
this was implemented due to computational limitations during experimentation.
The budget can also be adjusted and is set on line 10 of firefighter.py.
The maximum time is set in the loadGraph function in firefighter.py
as T = n however most solutions fall well below this limit.

The expected format of benchmark instances is the same as those found at
https://www.ic.unicamp.br/~cid/Problem-instances/Firefighter-in-Graphs/
however custom instances can use the following format:
 - Number of nodes on line 2
 - Initial fire locations on line 4
    - This can be a set of integers < n separated by spaces
    - Or "degree" or "d" for the highest degree node
 - u v from line 6 onwards
    - u and v are nodes < n with an edge between them in G
    - and should be separated by a space
