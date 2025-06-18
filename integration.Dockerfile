# Setup and then serve the backend
FROM python:3.12
WORKDIR /app
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy over the python files
COPY . ./tests/

# Execute the pytests
CMD sh -c "cd /app/tests/ && sleep 60 && PYTHONDONTWRITEBYTECODE=1 pytest -vv -p no:cacheprovider -s"
