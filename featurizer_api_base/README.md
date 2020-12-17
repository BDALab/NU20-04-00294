# Featurizer API Base
This package provides a base template for modern RESTFull featurizer API created using Python programming language and [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) library. It is developed by the members of [Brain Disease Analysis Laboratory](http://bdalab.utko.feec.vutbr.cz/). For more information, please contact: Zoltan Galaz <galaz@feec.vutbr.cz>.

## Requirements
Features extraction library must be installed separately (it is not a part of the `requirements.txt` file). The name of the library must be specified in `api/.env` file as `FEATURES_EXTRACTION_LIBRARY="library_name"`. After these two steps, the features can be extracted. To see the interface for the features computation class that needs to be used, see `api/dsp/interfaces/features_extraction.py`.

## Installation
```
# Clone the repository
git clone https://github.com/BDALab/featurizer_api_base.git

# Install packaging utils
pip install --upgrade pip
pip install --upgrade virtualenv

# Change directory
cd featurizer_api_base

# Activate virtual environment
# Linux
# Windows

# Linux
virtualenv .venv
source .venv/bin/activate

# Windows
virtualenv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
