# Intro

This is just to see how your code is being tested, you don't need to use or upload any of the code

# Run autograder locally
https://gradescope-autograders.readthedocs.io/en/latest/manual_docker/#running-autograder-images-locally


# Cheatsheet 

## Use without Docker

```
File Structure 

/compilers/ # this repo
/submission # built homework
    /cs8803_bin
        tigerc or tigerc.jar
/results # empty table
```

```
Bash Commands

cd compilers
python3 source/main.py hw=2

```

## Docker Build
```
docker buildx build --platform linux/amd64 . -t {image_name}  --build-arg s3_pub_key="z" --build-arg s3_prv_key="z"  --progress=plain  --build-arg hw="{homework number 1|2|3}"
```
## Run docker and connect bash
```
docker run -it  {image_name}  bash
```

## List running dockers to find {container_id}
```
docker ps
```

## Copy in docker
```
docker cp ~/PycharmProjects/compilers/submission {container_id}://autograder
```
