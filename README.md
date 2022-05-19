# Environment setup

## Create virtual environment for tests execution
```bash
python3 -m venv env
pip install -r requirements.txt
```

## Deploy and configure Data Quality solution
Follow [instructions](README.md)

## Run pytest tests
```bash
pytest --html=pytest_report.html
```

# View logs and reports
To view the reports, open file 'pytest_report.html'.
