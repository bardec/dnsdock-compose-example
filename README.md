# dnsdock + docker-compose example

An example of how to use [dnsdock](https://github.com/tonistiigi/dnsdock) with [Docker Compose](https://docs.docker.com/compose/).

## Usage

```sh
$ docker-compose up
```

![](https://andystanton.github.io/dnsdock-compose-example/dnsdock_small.gif)

## Problem

The following ```docker-compose.yml``` won't work because of circular references (ping depends on pong and pong depends on ping):

```yml
ping:
    ...
    links:
        - pong

pong:
    ...
    links:
        - ping
```

## Solution

dnsdock can be used to provide a DNS server that monitors containers in the Docker host and dynamically names them. This example shows one web server pinging another when its endpoint is hit and vice versa, with each server finding the other resolving the name of the other via a dnsdock instance.

In essence, the solution looks like this:

```yml
dnsdock:
    image: tonistiigi/dnsdock
    volumes:
        - /var/run/docker.sock:/run/docker.sock
    ports:
        - 172.17.42.1:53:53/udp

ping:
    ...
    environment:
        - DNSDOCK_NAME=ping
        - DNSDOCK_IMAGE=dnsdock
    dns: 172.17.42.1

pong:
    ...
    environment:
        - DNSDOCK_NAME=pong
        - DNSDOCK_IMAGE=dnsdock
    dns: 172.17.42.1
```

The ping container can now be identified by other containers as ```ping.dnsdock.docker``` and the pong container as ```pong.dnsdock.docker```.

The DNS can be added globally in the Docker host, or set when running individual containers. The individual approach suits me better as I don't want to run a dnsdock container all the time. Setting the DNS for individual containers is easily achieved with Docker Compose as demonstrated above.
