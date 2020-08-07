FROM python:3.7-buster

RUN apt update && DEBIAN_FRONTEND=noninteractive
RUN apt install -yq locales

ENV LANG="pt_BR.UTF-8"

RUN pip3 install flask gunicorn jsonpickle requests
RUN locale-gen pt_BR.UTF-8

ENV DEPLOYMENT_NAME="openalpr"
ENV CLIENT_CRT="/keys/client-admin.crt"
ENV CLIENT_KEY="/keys/client-admin.key"
ENV SERVER_CRT="/keys/server-ca.crt"
ENV SSH_PRIVATE_KEY="/keys/id_rsa"
ENV SSH_USER="ngd"
ENV NUM_THREADS="16"
ENV REFRESH_SECONDS="1"
ENV API_SERVER="https://192.168.1.134:6443"
ENV SELF_SERVER="http://localhost:4568"

WORKDIR /keys

COPY ./keys /keys

WORKDIR /project

COPY src .

EXPOSE 4568

#CMD ["flask", "run", "--host=0.0.0.0", "--port=4568"]
CMD ["gunicorn", "-w=64", "--threads=1", "--bind=0.0.0.0:4568", "app:app"]

