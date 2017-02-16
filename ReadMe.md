DESCRIPTION
-----------

The access log reporter is a Python 3 package that produces a report of the top 10 countries and US states that visited the site, how many visitors came from each country or state, and the most visitied page from each country or state. If there are multiple pages that tie for the most visited page, the first page alphabetically is returned.


INSTALLATION
------------

The access log reporter package can be installed by first cloning the repository:

    git clone https://gitlab.com/kstephens-/reporter.git

Then run the Python setup command with the install option inside the reporter directory.

    cd reporter
    python setup.py install


RUNNING THE REPORT
------------------

The access log reporter package provides a command line utility `access-report` which collects statistics for a single log file.

    usage: access-report [-h] [-d [DATABASE]] [-f [FILE]]

    run access report

    optional arguments:
      -h, --help            show this help message and exit
      -d [DATABASE], --database [DATABASE]
                            path to maxmind database file
      -f [FILE], --file [FILE]
                            path to log file to process


TESTS
_____

To run the tests, simply run the setup command with the test option inside the reporter directory.

    cd reporter
    python setup.py test


