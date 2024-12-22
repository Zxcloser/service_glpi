FROM python:3.12 AS builder

COPY requirements.txt .

RUN pip install --user -r requirements.txt

FROM python:3.12

WORKDIR /service_glpi

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY . .

CMD ["python", "-u", "main.py"]
