# Countach

![Test](https://github.com/HWRacing/countach/actions/workflows/test.yml/badge.svg)

Countach is software for extracting data from A2L files. At the moment it only works with A2L files generated for the Ecotrons EV2274A VCU by EcoCoder.

To use this package, import it using `import countach`. Call the function `countach.extractData(file)`, supplying the input file as an argument, and it will return the data from the file.

For documentation on the code, please see the following pages:

- [Documentation for `fileops.py`](docs/fileops.md)
- [Documentation for `processing.py`](docs/processing.md)
