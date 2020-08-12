FROM python:3.7-buster

RUN apt update && DEBIAN_FRONTEND=noninteractive
RUN apt install -yq locales

ENV LANG="pt_BR.UTF-8"

RUN pip3 install flask gunicorn jsonpickle requests
RUN locale-gen pt_BR.UTF-8

ENV CLIENT_CRT="/keys/client-admin.crt"
ENV CLIENT_KEY="/keys/client-admin.key"
ENV SERVER_CRT="/keys/server-ca.crt"
ENV SSH_PRIVATE_KEY="/keys/id_rsa"

WORKDIR /keys

COPY ./keys /keys

WORKDIR /project

COPY src .

EXPOSE 4570

#CMD ["flask", "run", "--host=0.0.0.0", "--port=4570"]
CMD ["gunicorn", "-w=64", "--threads=1", "--bind=0.0.0.0:4570", "app:app"]

