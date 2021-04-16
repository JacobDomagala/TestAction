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

# RUN pip3 install --no-cache --upgrade pip wheel && \
#     pip3 install --no-cache pandas numpy matplotlib PyGithub requests


FROM jdomagala/docker_with_matplotlib:latest

WORKDIR /src
COPY . /src

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY generate_graph.py /
RUN chmod +x /generate_graph.py

COPY generate_wiki_page.py /
RUN chmod +x /generate_wiki_page.py

ENTRYPOINT ["/entrypoint.sh"]
