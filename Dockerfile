FROM ubuntu:18.04

WORKDIR /project

RUN apt update && DEBIAN_FRONTEND=noninteractive
RUN apt install -yq openalpr openalpr-daemon openalpr-utils libopenalpr-dev python3 python3-pip python3-openalpr locales
RUN pip3 install flask
RUN locale-gen pt_BR.UTF-8 && cp -a /usr/share/openalpr/runtime_data/ocr/tessdata/*.traineddata /usr/share/openalpr/runtime_data/ocr/

ENV LANG="pt_BR.UTF-8"

COPY src .

CMD ["flask", "run", "--host=0.0.0.0", "--port=4568"]
