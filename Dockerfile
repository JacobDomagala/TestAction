FROM docker:20.10.5

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY generate_graph.py /
RUN chmod +x /generate_graph.py

COPY Dockerfile /
RUN chmod +x /Dockerfile

# Install all required packages like git/python/matplotlib
RUN apt-get update && apt-get install -y \
    python3 python3-pip
RUN pip3 install matplotlib PyGithub requests numpy wget

ENTRYPOINT ["/entrypoint.sh"]
