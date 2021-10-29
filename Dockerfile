FROM docker.io/python:3.8.12-slim-buster as builder

RUN apt update && \
    apt install -y --no-install-recommends \
    git && \
    apt clean &&\
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN python3 -m pip install --no-cache-dir --progress-bar off -U pip setuptools wheel && \
    python3 -m pip install --progress-bar off .

FROM docker.io/python:3.8.12-slim-buster

RUN apt update && \
    apt install -y --no-install-recommends \
    tini && \
    apt clean &&\
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin/cwl-inputs-parser /usr/local/bin/cwl-inputs-parser

WORKDIR /app
COPY . .

EXPOSE 8080

ENTRYPOINT ["tini", "--"]
CMD ["cwl-inputs-parser", "--server"]
