FROM ubuntu:latest

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY generate_graph.py /
RUN chmod +x /generate_graph.py

COPY Dockerfile /
RUN chmod +x /Dockerfile

RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# Install all required packages like git/python/matplotlib
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
RUN apt-get install -y \
    python3 python3-pip git docker-ce docker-ce-cli containerd.io
RUN pip3 install matplotlib PyGithub requests numpy wget

ENTRYPOINT ["/entrypoint.sh"]
