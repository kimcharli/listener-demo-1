# docker listener-demo-1

skeleton demo image for AppFormix listener


### Install

```sh
docker pull kimcharli/listener-demo-1:latest
```


### Credentials


### Run and test

```sh
docker run --rm --name listener -p 7070:7070 -it listener
```


From outside, run curl command against the application in the container for connectivity
```sh
curl -X POST -H "Content-Type: application/json" -d '{ "aa": "bb" }' http://<container-ip>:7070
```


Test listener script in AppFormix





