FROM python:3.7-buster

ENV DEBIAN_FRONTEND="noninteractive"
ENV LANGUAGE="pt_BR.UTF-8"
ENV LC_ALL="pt_BR.UTF-8"
ENV LANG="pt_BR.UTF-8"

RUN apt update && apt install -yq locales
RUN locale-gen pt_BR.UTF-8 && localedef -i pt_BR -f UTF-8 pt_BR.UTF-8 && dpkg-reconfigure locales
RUN apt install -yq libopencv-dev python3-opencv
RUN pip3 install flask gunicorn

WORKDIR /libfacedetection
COPY libfacedetection .
RUN ./build.sh lib && ./build.sh deploy

WORKDIR /project
COPY src .

EXPOSE 4568

CMD ["flask", "run", "--host=0.0.0.0", "--port=4568", "--without-threads"]
#CMD ["gunicorn", "-w=`nproc`", "--threads=1", "--bind=0.0.0.0:4568", "app:app"]
