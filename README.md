# Build
docker build -t compilerhw1 --build-arg s3_pub_key="z" --build-arg s3_prv_key="z"

# Run docker and connect bash
docker run -it  compilerhw1  bash

# List running dockers
docker ps

# Copy in docker
docker cp ~/PycharmProjects/compilers/submission {container_id}://autograder