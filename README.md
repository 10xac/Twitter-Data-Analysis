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

### So here are the bare minimum requirement for completing this task

1. Fork repository to your github account
2. Create a branch called “fix_bug” to fix the bugs in the fix_clean_tweets_dataframe.py and fix_extract_dataframe.py 
3. In branch `fix_bug` copy or rename `fix_clean_tweets_dataframe.py` to `clean_tweets_dataframe.py` and `fix_extract_dataframe.py`  to `extract_dataframe.py` 
4. Fix the bugs on `clean_tweets_dataframe.py` and `extract_dataframe.py` 
5. Multiple times push the code you are working on to git, and once the fix is complete, merge the `fix_bug` branch to master
6. Create a new branch called `make_unittest` for creating a new unit test for extract_dataframe.py code.
7. After completing the unit test writing, merge  “make_unittest”  to main branch
8. In all cases when you merge, make sure you first do Pull Request, review, then accept the merge.
9. Setup Travis CI to your repository such that when you git push new code (or merge a branch) to the main branch, the unit test in tests/*.py runs automatically. 10. All tests should pass.

After Completing this Challenge, you would have explore  

- Unittesting
- Modular Coding
- Software Engineering Best Practices
- Python Package Structure
- Bug Fix (Debugging)

Have Fun and Cheers
