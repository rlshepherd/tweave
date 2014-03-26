grappler
===
Connects and accepts data from a Twitter Streaming API v1.1
endpoint based on a user-supplied list of keywords. Writes to
a database and/or JSON file (via tweave.py).

Grappler handles authorization, but you must provide your own tokens
in <streamsettings.py>. Tokens can be obtained via Twitter:
https://dev.twitter.com/docs/auth/tokens-devtwittercom

Usage:  

    grappler.py db <database> <table> [-j] [--bind] stream <keyword>...
    grappler.py json <filename> [--bind] stream <keyword>...
    grappler.py -v | --version
    grappler.py -h | --help

Options:
 
    -h --help    Show this screen.
    --version    Show version.
    -j           Auxiliary JSON output.
    --bind       Limit results to geoenabled tweets from PH.
  
**Examples**:

1. Save all tweets containing 'hashtag' to test.json:

        python grappler.py json test.json stream hashtag

2. Save all tweets containing 'hashtag' to both the database
and hashtag.json (name defaults to first keyword).:

        python grappler.py db myprojectdb mytable -j stream hashtag

3. Limit your search results to geotagged tweets originating
   from the Philippines:

        python grappler.py db myprojectdb mytable --bind stream hashtag

## Installation

Grappler is built using python and SQLite3. If you're new to python, or don't use pip, virtualenv and virtualenv-wrapper, please read **Preperation** first. If you're a python wiz, skip to **Install**.


### Preperation: 

1. Install pip, virtualenv, virtualenv-wrapper  
 
        sudo apt-get install python-pip  
        sudo pip install virtualenv  
        mkdir ~/.virtualenvs  
        sudo pip install virtualenvwrapper
        export WORKON_HOME=~/.virtualenvs

2. Make virtualenv wrapper commands available at the terminal, add this to the end of ~/.bashrc:

        . /usr/local/bin/virtualenvwrapper.sh

    Exit and re-open your shell.

3. Make a new virtualenv for this project:

        mkvirtualenv grappler

### Install

4. Clone the repo (requires authorized bitbucket account):

        cd ~/yourworkingdirectory/  
        git clone https://username@bitbucket.org/rlshepherd/grappler.git

7. Install python dependencies: 

        cd grappler  
        pip install -r requirements.txt

8. If you get a non-zero exit status for pycurl, try: 

        sudo apt-get install libcurl4-gnutls-dev librtmp-dev  
        sudo env ARCHFLAGS="-arch x86_64" pip install pycurl  

9. Install the SQLite3 command line tool and initialize a db (not in project directory)  

        sudo apt-get install sqlite3  
        cd ../  
        sqlite3 test.db  
        sqlite> .tables  
        sqlite> .exit  