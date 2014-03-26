#! /usr/local/bin/pythonw
"""
tweave.py
===========
Connects and accepts data from a Twitter Streaming API v1.1
endpoint based on a user-supplied list of keywords. Writes to
a database and/or JSON file (via tweave.py).

Grappler handles authorization, but you must provide your own tokens
in <streamsettings.py>. Tokens can be obtained via Twitter:
https://dev.twitter.com/docs/auth/tokens-devtwittercom

Usage:
  tweave.py db <database> <table> [-j] [--bind] stream <keyword>...
  tweave.py json <filename> [--bind] stream <keyword>...
  tweave.py -v | --version
  tweave.py -h | --help

Options: 
  -h --help    Show this screen.
  --version    Show version.
  -j           Auxiliary JSON output.
  --bind       Limit results to geoenabled tweets from PH.

Examples:
=========
1.Save all tweets containing 'hashtag' to test.json:

python tweave.py json test.json stream hashtag

2. Save all tweets containing 'hashtag' to both the database
and hashtag.json (name defaults to first keyword).:

python tweave.py db myprojectdb mytable -j stream hashtag

3. Limit your search results to geotagged tweets originating
   from the Philippines:

python tweave.py db myprojectdb mytable --bind stream hashtag

"""

import cmd
import datetime
from docopt import docopt
import logging
from os import path
import sqlite3 as lite
import streamsettings as keys
import threading
from streamlistener import TwitterStream as TwitterStream

class StopCmd(cmd.Cmd):
  def do_stop(self, message):
    print "Stopping tweave...\n"
    return(1)
  def do_count(self, message):
  	print "Tweets saved so far: %s \n" % keys.count
  	print "Errors so far: %s \n" % keys.errors

class Tweave(threading.Thread):
  """Thread subclass for TwitterStream class
  """
  def run(self):
    ts = TwitterStream(post_params, database, table, outfile)
    ts.start()
  def stop(self):
    keys.user_interrupt = True
    logging.info('Stop signal sent.')

if __name__ == '__main__':
  # Logging
  logging.basicConfig(filename='tweave.log', level=logging.INFO,
                      format='%(asctime)s %(message)s',
                      datefmt='%d/%m/%Y %I:%M:%S %p')
  logging.info('STARTED')

  # Validate inputs:
  arguments = docopt(__doc__, version='Tweave v0.1')

  # Number of filter keywords.
  if len(arguments['<keyword>']) >= 400:
    logging.error('Too many keywords. 400 key words max.')
    raise Exception('Max of 400 keywords, you entered %s'
                     % (len(arguments['<keyword'])))

  if arguments['db']:
    if path.isfile('%s.db' % (arguments['<database>'])):
        database = arguments['<database>']
        table = arguments['<table>']
        con = lite.connect('%s.db' % database)
        with con:
          cur = con.cursor()    
          cur.execute('create table if not exists %s (tweet_id INT, created_at TEXT, user_id_str TEXT, user_screen_name TEXT, retweeted_id INT, message TEXT, long REAL, lat REAL, media_url TEXT)'
                       % (table))
        if arguments['-j']:
          outfile = '%s.json' % arguments['<keyword>'][0]
        else:
          outfile = False
    else:
      logging.error('Could not connect to database.')
      raise Exception('Could not find database: %s'
                      %(arguments['<database>']))
  elif arguments['json']:
    database = False
    table = False
    outfile = arguments['<filename>']

  post_params = {'include_entities': 1,
                 'stall_warning': 'true',
                 'track': ', '.join(arguments['<keyword>'])}

  if arguments['--bind']:
    post_params = {'locations' : '115, 5, 130, 22'}

  logging.info('Keywords: %s' % (', '.join(arguments['<keyword>'])))
  tweave = Tweave()
  tweave.start()
  logging.info('Begin listening.')
  print 'Tweave listening now:\n'
  print 'Keywords: %s' % ', '.join(arguments['<keyword>'])
  if arguments['--bind']:
    print 'Bound to PH location-enabled tweets' 
  print '\n-----------------------------------------------------------------'
  print 'Access token key: %s' % keys.OAUTH_KEYS['access_token_key']
  print 'Access token secret: %s' % keys.OAUTH_KEYS['access_token_secret']
  print 'Consumer key: %s' % keys.OAUTH_KEYS['consumer_key']
  print 'Consumer secret: %s' % keys.OAUTH_KEYS['consumer_secret']
  print '-----------------------------------------------------------------'
  print '\nType \'count\' to see numer of saved tweets.'
  print '\nType \'stop\' to stop collection and exit.'
  waiting = StopCmd()
  waiting.prompt = '(Tweave): '
  waiting.cmdloop()
  grappler.stop()
  grappler.join()
  logging.info('FINISHED')
  print 'Finished and exiting.'
