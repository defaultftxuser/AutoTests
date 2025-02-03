FROM python:3.12-bookworm

RUN curl -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.32.0/allure-commandline-2.32.0.tgz | \
    tar -xz -C /opt/ && \
    ln -s /opt/allure-2.32.0/bin/allure /usr/bin/allure

WORKDIR /usr/workspace

COPY ./requirements.txt /usr/workspace

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps