# cardiffmet-dat5004-prac1
**Assessment Code:** PRAC1

**Author:** Tom Rowan, ST20285213

**Course:** DAT5004_S2_24

**Course Tutor:** Dr. Sandeep Singh Sengar

This README file includes details on how to access and run each of the three tasks that form this assessment.

**Files included:**

| Filename | Purpose |
|--|--|
| DAT5004-S2_24-Prac1-Task1-ST20285213-TomRowan.ipynb | Task 1 Notebook |
| DAT5004-S2_24-Prac1-Task2-ST20285213-TomRowan.py | Task 2 Cricketers Database Program |
| cricketers.db | Sample Database for cricketers program. |
| table.html | Sample data from https://www.espncricinfo.com/ to populate the cricketers program. | 
| DAT5004-S2_24-Prac1-Task3-ST20285213-TomRowan.ipynb | Task 3 Notebook |
| screenshot_cluster_creation.png | MongoDB Cluster Created - Screenshot |
| screenshot_titanic_data_in_cluster.png | Data Uploaded to MongoDB Cluster - Screenshot |
| requirements.txt | Python libraries required |

NB: The requirements.txt file includes all the python libraries needed for all three tasks.

## Task 1 - Extracting Movie Information from FilmCrave.com

The task being answered is as follows:

> FilmCrave (https://www.filmcrave.com/list_top_movie.php) is a website where people share their favourite
movies, reviews, and ratings. It has a huge collection of films, complete with rankings, genres, and other details.

> The goal of this project is to gather information on over 1,000 movies from this site. The data we want includes the
Year of Release, Overall Rating, Language, Genre, MPAA Rating (like PG or R), Director, Actors, and a short Plot
summary.

**Format:** Jupyter Notebook (.ipynb file)

**How to run the code:**
The code is provided in a Jupyter notebook. The code has already been run through, and the results should already be in place in the saved notebook.

However, if the reviewer wishes to rerun the code, this is possible provided that the requirements are available in the python environment. 

As provided, it **will not** run a live scraping exercise against the website. This is because this function is controlled by two variables, which are set to False in the file provided.

```
_FULL_WEB_SCRAPE_ = False
_TOP1000_WEB_SCRAPE_ = False
```

If the first is set to True, the notebook will run a web scrape of some 57,000 movies. This will take eight hours and is not recommended to be repeated. This has been run once, and the dataset is used in the analysus phase.

Please note that the notebook reaches out to the Internet to retrieve this dataset for the analysis phase of the task. 

This dataset is located at:

[https://datascience.daemonchild.com/year2/dat5004/prac1/datasets/movie_data_all_utf8.csv](https://datascience.daemonchild.com/year2/dat5004/prac1/datasets/movie_data_all_utf8.csv)

If the second is set to True, the notebook will perform a web scrape for the Top 1000 movies. This will take 10-15 minutes depending on the performance of your computer and the website itself.


## Task 2 - Cricketers Database using SQLite3

**Format:** Python File (.py file)

###How to run the code:
The python file can be run as follows from a terminal:

```
python3 DAT5004-S2_24-Prac1-Task2-ST20285213-TomRowan.py


           _      _        _                      _       _        _                  
  ___ _ __(_) ___| | _____| |_ ___ _ __ ___    __| | __ _| |_ __ _| |__   __ _ ___  ___ 
 / __| '__| |/ __| |/ / _ \ __/ _ \ '__/ __|  / _` |/ _` | __/ _` | '_ \ / _` / __|/ _ \
| (__| |  | | (__|   <  __/ ||  __/ |  \__ \ | (_| | (_| | || (_| | |_) | (_| \__ \  __/
 \___|_|  |_|\___|_|\_\___|\__\___|_|  |___/  \__,_|\__,_|\__\__,_|_.__/ \__,_|___/\___|
 
     by Tom Rowan, ST20285213

-- Opening database cricketers.db

   Cricketers Database - Main Menu   
-------------------------------------
-- Required Options --
  1. Insert Cricketer
  2. View All Cricketers
  3. Find Cricketer by Name
  4. Find Best Score (on 'High Score')
  5. Update Cricketer
  6. Delete Cricketer

-- Extended Menu --
 10. Find Cricketers by Country
 11. List Top 10 Cricketers by High Score
 12. List Top 10 Cricketers by Batting Average
 13. List Top 10 Cricketers by Matches Played
 14. List Top 10 Cricketers by Runs Scored

-- Program Options --
 90. Load example data from HTML file (table.html)

 99. Quit
Select an option: 
```

### Menu Options
The menu options are relatively self explanatory. The menu is broken down into three sections.

1) Required Options - these options are specified by the Task Description.
2) Extended Menu - these options are in addition to the requirements of this Task.
3) Program Options

The program options are as follows:

90) Uses the provided 'table.html' file to populate the data with sample data. This file was saved from the [https://www.espncricinfo.com/](https://www.espncricinfo.com/) website, which provides various cricketing data. This site resists being web scraped programatically using python, returning a '403' error code when attempted. However, saving the data from the page [https://www.espncricinfo.com/records/most-runs-in-career-223646](https://www.espncricinfo.com/records/most-runs-in-career-223646) allows for parsing this data into a useful format.

The provided cricketers.db file includes this data already. However, you are welcome to attempt to add the data a second time (which should fail gracefully as the database doesn't allow duplicates.)

99) Quit the program.


## Task 3 - MongoDB and the Titanic Dataset

**Format:** Jupyter Notebook (.ipynb file)

**How to run the code:**
The code is provided in a Jupyter notebook. The code has already been run through, and the results should already be in place in the saved notebook.

However, if the reviewer wishes to rerun the code, this is possible provided that the requirements are available in the python environment. 

The MongoDB cluster has been created as shown here:

<img src='https://datascience.daemonchild.com/year2/dat5004/prac1/images/screenshot_cluster_creation.png' width=75%/>

Data has been uploaded as shown here:

<img src='https://datascience.daemonchild.com/year2/dat5004/prac1/images/screenshot_titanic_data_in_cluster.png' width=75%/>

(These screenshots are included in the submission folder.)

When the notebook runs, it checks for existence of the database in the cluster and will not upload the dataset a second time to avoid duplication. 



