FROM python:3.9
WORKDIR /
COPY test_DB_AdventureWorks2017.py ./
CMD ["python", "./test_DB_AdventureWorks2017.py"]