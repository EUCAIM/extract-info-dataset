# Extract information fro mone or more datasets

This repository contains the necessary files needed to create a repository compliant Docker image that allows the execution of the datasets information extractor.

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