FROM kimcharli/appformix-installer-base:0.0.1

LABEL maintainer="kimcharli@gmail.com"

WORKDIR /root
COPY requirements.txt setup.sh listener.py /root/

RUN sh setup.sh

EXPOSE 22 7070

ENTRYPOINT ["/usr/sbin/sshd", "-D"]


