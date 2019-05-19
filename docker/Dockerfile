FROM hysds/usgs-base:latest
MAINTAINER jlinick "Justin.P.Linick@jpl.nasa.gov"
LABEL description="Ingest products from metadata"

yum -y install unzip

USER ops

COPY . /home/ops/verdi/ops/eo1_ali

WORKDIR /home/ops
CMD ["/bin/bash", "--login"]

