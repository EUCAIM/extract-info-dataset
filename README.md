# Extract information from one or more datasets

This repository contains the necessary files needed to create a repository compliant Docker image that allows the execution of the datasets information extractor.

## Building

This application is based on the ubuntu-python Docker image that contains all the necessary setup to be compliant to our repository's rules.
Since this image can be located in various Docker repositories, we allow the specification of the path of the base image when building with Docker.
The following command can be used to create the image (using the Harbor in CHAIMELEON as the Docker repository, change it as needed):
```
   docker build --tag extract-info-dataset:latest --build-arg BASE_IMG=harbor.chaimeleon-eu.i3m.upv.es/chaimeleon-library-batch/ubuntu-python:latest -f Dockerfile ./
```

## Execution

The first argument has to be the path where the datasets are.
Following the path, you can optionally also pass one or more of these arguments:

```
    -v/--verbose - Show all info on screen about the creation process of the dictionaries. 
    -f/--manufacturers - It Shows all manufacturers in a dataset.
    -b/--bodyparts - It Shows all body parts included in a dataset.
    -s/--numberseries - It Shows number of series.
```

Therefore, to get the most information possible for all datasets mounted in the repository's predefined path you can execute:

```
    docker run extract-info-dataset:latest /home/chaimeleon/datasets -s -f -b -v
```

Using jobman:

```
    jobman submit -i extract-info-dataset:latest -j extract-info -- /home/chaimeleon/datasets -s -f -b -v
```

and get the actual output of the operation (once completed) with:

```
    jobman logs -j extract-info
```