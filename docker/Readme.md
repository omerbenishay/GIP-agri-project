### Building the docker

```docker build -t nomios/leafsegmentor .```

### Running the docker

```docker run -it --runtime=nvidia --name leafsegmentor -v <working dir>:/workspace nomios/leafsegmentor &```

### Shell

```docker exec -it leafsegmentor /bin/bash```