FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

EXPOSE 5061

COPY ./app /app

RUN pip install -r requirements.txt

ENV PORT=5061

CMD ["uvicorn", "main:cognitus", "--host", "0.0.0.0", "--port", "5061"]