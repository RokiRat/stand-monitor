FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && \
    apt-get install -y procps && \
    groupadd -g 10000 python_runer && \ 
    useradd python_runer -u 10000 -g python_runer -s /bin/bash -m

USER python_runer
WORKDIR /home/python_runer
COPY app/server.py .
CMD [ "python3", "server.py" ]

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:8080/health || exit 1