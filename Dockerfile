FROM ubuntu:latest

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY generate_graph.py /
RUN chmod +x /generate_graph.py

# Install all required packages like git/python/matplotlib
RUN apt-get update && apt-get install -y \
    python3 python3-pip git
RUN pip3 install matplotlib PyGithub requests numpy wget

ENTRYPOINT ["/entrypoint.sh"]
