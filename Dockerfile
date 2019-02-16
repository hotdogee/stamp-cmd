FROM buildpack-deps:jessie

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ENV PYTHON_VERSION 2.7.9

RUN apt-get update

RUN apt-get install -y python-qt4 libblas-dev liblapack-dev gfortran freetype* python-pip python-dev

RUN pip install --upgrade numpy scipy 'matplotlib>=2.2.3,<3.0.0'

RUN pip install stamp

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./stamp_cmd.py /usr/src/app
COPY ./AbstractGroupPlotPlugin.py /usr/local/python2.7/dist-packages/stamp/plugins/groups
COPY ./ExtendedErrorBar.py /usr/local/python2.7/dist-packages/stamp/plugins/groups/plots

# run the command
ENTRYPOINT ["python". "stamp_cmd.py"]
CMD ["-h"] 