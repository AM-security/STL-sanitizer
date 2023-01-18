## How to build:

### Resolve dependencies:
        pip install git+https://github.com/AM-security/STL-channels-encoder
### Add the library folder to the python interpreter path
        pip show stlcovertchannels  # to see the location of the library
        Add the location the python interpreter paths
        In my case the location is <...local/lib/python3.9/site-packages>
        Follow this instructions to add the path:
            https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-reloading-interpreter-paths.html



## Tests:
    cd sanitizer_random/tests && pytest -q sanitizer_random_test.py