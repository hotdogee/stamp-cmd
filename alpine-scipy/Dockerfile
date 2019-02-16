FROM reelio/alpine-scipy

LABEL maintainer="Han Lin <hotdogee@gmail.com>"

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y \
    python-qt4 \
    libblas-dev \
    liblapack-dev \
    freetype* \
    && pip install --upgrade 'matplotlib>=2.2.3,<3.0.0' \
    && pip install stamp \
    && mkdir -p /usr/src/app \
    && mkdir -p /data

WORKDIR /data

COPY ./stamp_cmd.py /usr/src/app
COPY ./AbstractGroupPlotPlugin.py /usr/local/lib/python2.7/dist-packages/stamp/plugins/groups
COPY ./ExtendedErrorBar.py /usr/local/lib/python2.7/dist-packages/stamp/plugins/groups/plots

# run the command
ENTRYPOINT ["python", "/usr/src/app/stamp_cmd.py"]
CMD ["-h"] 