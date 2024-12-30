# ABECornhole

## Overview
There are currently two projects in this repository. They will be described below. The intentions is to eventually build these together into one application.

### stats.py
The first project in this repository is a python script 'scripts.py', which will take an excel spreadhseet as input and store all of its data into a pandas DataFrame. The input will contain the following information:
1. Player Names
2. Player's number of weeks attended
3. Player's score for each week (each week has its own column)
   
We will then use this information to calculate each player's:
1. Average of best 5 weeks
2. Total weekly average
Once these calculations are complete, players will be sorted by their average of their best 5 weeks, and exported to an excel file. 

We will have a main datasheet that stores each person's score for each week. We will then dump results into a file each week that contains the above mentioned information. Currently this is all being run out of google colab.

### Data Stuff
The second project in this repository is a data viewing application. Its intention is to eventually allow users to visually view their performance across a season or all seasons. There are various forms of data that users can view. They will be written up below.

#### Database
The 'database' is a collection of comma separated value (CSV) files, each representing a table. The main table (main.csv) stores all data used by this application. It may be separated at some point but I currently don't have a need for separation. The two other tables **Players.csv** and **Alias.csv** store player names and scoreholio 'alias' names respectively. The Alias names are simply other names a player has used in Scoreholio. This allows us to enter data for one user under multiple names. The Players table stores an index (primary key) that links each person's name to a number. The Alias table then uses Index as a foreign key to connect known Scoreholio names to a person's name. Each Table has its own associated script that helps fetch and update data in that table. 

##### Players.csv
- **col name**:

##### Alias.csv
- **col name**:

##### main.csv
- **col name**: 
