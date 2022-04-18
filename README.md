# Intro

This is just to see how your code is being tested, you don't need to use or upload any of the code

# Run autograder locally
https://gradescope-autograders.readthedocs.io/en/latest/manual_docker/#running-autograder-images-locally


# Cheatsheet 

## Use without no Docker

```
Structure 

/compilers/ # this repo
/submission # built homework
    /cs8803_bin
        tigerc or tigerc.jar
/results # empty table
```
```
cd compilers
python3 source/main.py hw=2

```

## Docker Build
```
docker buildx build --platform linux/amd64 . -t zz:h2  --build-arg s3_pub_key="z" --build-arg s3_prv_key="z"  --progress=plain  --build-arg hw="2"

## Run docker and connect bash
```docker run -it  compilerhw1  bash```

## List running dockers
```docker ps```

## Copy in docker
```docker cp ~/PycharmProjects/compilers/submission {container_id}://autograder```
