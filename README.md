# Extract information fro mone or more datasets

This repository contains the necessary files needed to create a repository compliant Docker image that allows the execution of the information extractor.

The python script accepts the following arguments (used as Docker's CMD):

```
    path - Root of the directory to analise.
    -v/--verbose - Show all info on screen about the creation process of the dictionaries. 
    -f/--manufacturers - It Shows all manufacturers in a dataset.
    -b/--bodyparts - It Shows all body parts included in a dataset.
    -s/--numberseries - It Shows number of series.
```

Therefore, to get the information for all datasets mounted in the repository's predefined path you can execute:

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