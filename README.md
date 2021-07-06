# Twitter-Data-Analysis

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites (Linux)
- Python

```bash
sudo add-apt-repository ppa:jonathonf/python-3.7
sudo apt-get update
sudo apt-get install python3.7
```

- pip3

```bash
sudo apt update
sudo apt install python3-pip
```



## Installing

### For Development

1. Clone the Repo
   ```bash
    git clone https://github.com/nebasam/Twitter-Data-Analysis.git
   ```
1. cd into repo
   ```bash
   cd Twitter-Data-Analysis
   ```
1. Install Requirements
   ```bash
    pip3 install requirements.txt
   ```
1. Extract dataframe
   ```bash
   python3 extract_dataframe.py
   ```
1. Clean Extracted DataFrame
   ```bash
   python3 clean_tweets_dataframe
   ```
1. Add Dataframe data into sql database  #pls add your databasename, db password, db username to db.yaml file first
   ```bash
   python3 data.py
   ```
3. Run the App
   ```bash
    streamlit run main.py


## Topic Modeling


Topic Modeling for twtter data can be found in twitter_modeling.ipynb jupyter notebook file.


## Unit Testing

The following code enables you ti run unit test

1. Get into Test Directory
```bash
   cd tests
   ```
1. Run Test
   ```bash
   python3 test_extract_dataframe.py
   ```
