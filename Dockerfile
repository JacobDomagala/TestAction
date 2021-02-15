FROM ubuntu:latest

#RUN apk add --no-cache bash findutils
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Install python/pip
# ENV PYTHONUNBUFFERED=1
# RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
# RUN python3 -m ensurepip

# RUN apk add --no-cache tesseract-ocr python3 py3-numpy && \
#     pip3 install --upgrade pip setuptools wheel && \
#     apk add --no-cache --virtual .build-deps gcc g++ zlib-dev make python3-dev jpeg-dev && \
#     pip3 install numpy scipy pandas matplotlib && \
#     apk del .build-deps

RUN apt-get update
RUN apt-get install python3 -y && apt-get install python3-pip -y
RUN pip3 install matplotlib

ENTRYPOINT ["/entrypoint.sh"]
