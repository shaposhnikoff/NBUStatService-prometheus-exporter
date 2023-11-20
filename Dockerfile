FROM python:3.11-slim-bullseye
RUN pip install --no-cache-dir prometheus_client requests
COPY currency.py /currency.py
EXPOSE 8000
CMD ["python", "/currency.py"]
