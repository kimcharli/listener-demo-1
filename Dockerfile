FROM kimcharli/appformix-installer:0.0.2

LABEL maintainer="kimcharli@gmail.com"

WORKDIR /root
COPY listener.py /root/

RUN pip install requests[security]==2.8.1 flask==0.10.1 flask-restful==0.3.5

EXPOSE 7070

CMD python /root/listener.py



