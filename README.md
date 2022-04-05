# Intro

This is just to see how your code is being tested, you don't need to use or upload any of the code

# Run autograder locally
https://gradescope-autograders.readthedocs.io/en/latest/manual_docker/#running-autograder-images-locally


# Cheatsheet 

## Build
```docker build -t compilerhw1 --build-arg s3_pub_key="z" --build-arg s3_prv_key="z"```

## Run docker and connect bash
```docker run -it  compilerhw1  bash```

## List running dockers
```docker ps```

## Copy in docker
```docker cp ~/PycharmProjects/compilers/submission {container_id}://autograder```
