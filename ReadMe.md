INSTALLATION
------------

The access log reporter package can be installed by first cloning the repository:

    git clone https://gitlab.com/kstephens-/reporter.git

Then run the Python setup command inside the reporter directory.

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


