FROM ubuntu:18.04

WORKDIR /project

RUN apt update && DEBIAN_FRONTEND=noninteractive
RUN apt install -yq openalpr openalpr-daemon openalpr-utils libopenalpr-dev python3 python3-pip python3-openalpr locales
RUN pip3 install flask gunicorn
RUN locale-gen pt_BR.UTF-8 && cp -a /usr/share/openalpr/runtime_data/ocr/tessdata/*.traineddata /usr/share/openalpr/runtime_data/ocr/

ENV LANG="pt_BR.UTF-8"

COPY src .

EXPOSE 4568

CMD ["flask", "run", "--host=0.0.0.0", "--port=4568", "--without-threads"]
#CMD ["gunicorn", "-w=`nproc`", "--threads=1", "--bind=0.0.0.0:4568", "app:app"]
