# docker listener-demo-1

skeleton demo image for AppFormix listener


### Install

```sh
docker pull kimcharli/listener-demo-1:latest
```


### Credentials

The password of `root` is `contrail123`


### Run and test

Run container from docker engine
```sh
docker run --name listener -d -p 0.0.0.0:7703:7070 -p 0.0.0.0:2203:22 kimcharli/listener-demo-1:latest
```

Log in to the container.
```sh
ssh -p 2203 root@<docker-engine-ip>
```


Run the application and monitor within the container
```sh
python listener.py

```

or
```sh
docker exec -it listener python listener.py
```


From outside, run curl command against the application in the container for connectivity
```sh
curl -X POST -H "Content-Type: application/json" -d '{ "aa": "bb" }' http://<container-ip>:7703
```


Test listener script in AppFormix





