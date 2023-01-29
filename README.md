# comet-brain



- Each django app has management/commands folder containing scripts testing the App's API











# Deprecated


The api which serves all of the Comet App interfaces

## AWS Deployment

- Registry `923405430231.dkr.ecr.us-east-2.amazonaws.com/comet-brain`


### Commands


##### AWS Docker Login

`aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 923405430231.dkr.ecr.us-east-2.amazonaws.com`



##### Local

`docker-compose build`

`docker-compose up -d`

`dshell comet-brain`

`. run_dev.sh`



##### Dev

`docker build -f DockerfileDev -t apazagab/comet-brain:latest .`

`docker run --network=comet-network --name=comet-brain apazagab/comet-brain:latest`



##### Prod

`docker build -f DockerfileProd -t 923405430231.dkr.ecr.us-east-2.amazonaws.com/comet-brain:latest .`

`docker push 923405430231.dkr.ecr.us-east-2.amazonaws.com/comet-brain:latest`











