FROM hysds/usgs-base:latest
MAINTAINER jlinick "Justin.P.Linick@jpl.nasa.gov"
LABEL description="Ingest products from metadata"

USER ops

sudo yum -y install unzip

COPY . /home/ops/verdi/ops/eo1_ali

WORKDIR /home/ops
CMD ["/bin/bash", "--login"]

