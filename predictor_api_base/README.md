# Predictor API Base
This package provides a base template for modern RESTFull predictor API created using Python programming language and [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) library. It is developed by the members of [Brain Disease Analysis Laboratory](http://bdalab.utko.feec.vutbr.cz/). For more information, please contact: Zoltan Galaz <galaz@feec.vutbr.cz>.

## Requirements
Serialized predictors should be stored in the following dir `api/ml/models`.

## Installation
```
# Clone the repository
git clone https://github.com/BDALab/predictor_api_base.git

# Install packaging utils
pip install --upgrade pip
pip install --upgrade virtualenv

# Change directory
cd predictor_api_base

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
