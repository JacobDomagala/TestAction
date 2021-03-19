# FROM ubuntu:latest

# RUN apt-get update && apt-get install -y \
#     apt-transport-https \
#     ca-certificates \
#     curl \
#     gnupg \
#     lsb-release \
#     software-properties-common

# RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# # Install all required packages like git/python/matplotlib
# RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
# RUN apt-get install -y \
#     python3 python3-pip git docker-ce docker-ce-cli containerd.io


FROM docker:stable

RUN apk add --update --no-cache make automake gcc g++ subversion python3-dev py3-pip zlib-dev jpeg-dev

RUN pip3 install --no-cache --upgrade pip wheel && \
    pip3 install --no-cache numpy matplotlib PyGithub requests

# RUN apk add --no-cache tesseract-ocr python3-dev py3-pip && \
#     pip3 install --upgrade pip setuptools wheel && \
#     apk add --no-cache --virtual .build-deps gcc g++ zlib-dev make py-numpy-dev jpeg-dev && \
#     pip3 install matplotlib requests PyGithub && \
#     apk del .build-deps

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY generate_graph.py /
RUN chmod +x /generate_graph.py

COPY Dockerfile /
RUN chmod +x /Dockerfile

#ENTRYPOINT ["/entrypoint.sh"]
