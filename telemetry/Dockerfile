FROM python:3.7-buster

RUN apt update && DEBIAN_FRONTEND=noninteractive
RUN apt install -yq locales sysstat

ENV LANG="pt_BR.UTF-8"

RUN pip3 install flask jsonpickle
RUN locale-gen pt_BR.UTF-8

WORKDIR /project

COPY src .

EXPOSE 4580

CMD ["flask", "run", "--host=0.0.0.0", "--port=4580"]
