# Instructions

## Build container

1. Run `./create_docker.sh`


### Troubleshooting
If it complains...
>  Network distro\_default declared as external, but could not be found.

Then - do `docker inspect` on any of the containers to find out the name of the network.

Example: 

```
docker inspect ca-mongo -f "{{json .NetworkSettings }}"
```

Edit docker-compose.yml and change "distro\_default" to the actual name of the network.

## Usage

1. Put input-files into `./app/tmp`.<br>
They will be mapped to `/app/tmp` in the container.

2. Run:

```
docker exec seg-loader /app/loadfiles.sh
```

* Pass the following 6 parameters:

```
.../loadfiles.sh pathdb-url collection study subject user password

```
