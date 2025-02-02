FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir playwright pytest pytest-asyncio allure-pytest \
    && playwright install --with-deps

WORKDIR /tests

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "--alluredir=/tests/allure-results", "--video=on", "--capture=sys", "--headless"]
