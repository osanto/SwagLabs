# Swag Labs
Swag Labs UI Automation

## Overview
This is a simple training project aimed at practicing UI automation with python. 
The application under test is [Swag Labs](https://www.saucedemo.com/), a sample e-commerce site. 
The project is built using the Page Object Model (POM) design pattern with Python, Selenium, and Pytest.

## Project Structure
SwagLabs
```
├── tests/ # Test cases
├── pages/ # Page object classes
├── config.py # Configuration file
├── README.md # Project documentation
└── requirements.txt # Dependencies file
```

## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Steps
1. Clone the repository:
   ``` 
   git clone https://github.com/osanto/SwagLabs.git
   ```
2. Create a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```
3. Install dependencies
   ``` 
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   Create a `.env` file in the project root and add the following (replace with your actual values):

   ```
   USER_NAME=your_username
   PASSWORD=your_password
   ```

### Usage
To run the tests, use the following command:
```
pytest
```

### Generating Test Reports
This project uses [pytest-html](https://github.com/pytest-dev/pytest-html) to generate detailed HTML reports for test results. To generate a report, run the tests with the following command:

```
pytest --html=report.html --self-contained-html
```