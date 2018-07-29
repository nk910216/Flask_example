#!/bin/bash
set -ex

MY_SQL_DOCKER_NAME="mysql-mithril-hw"
MY_SQL_DOCKER_VOLUME="mysql-mithril-hw-vol"
PASSWORD="rory7965"
MY_SQL_PORT="3307"
MY_NETWORK_NAME="mithrik-hw-net"
MY_SERVER_SECRET_KEY="change_this_to_secret_key"

# clean up - remove mysql docker and server docker
docker rm -f $MY_SQL_DOCKER_NAME || true
make rm || true

# create docker network for all service
docker network create $MY_NETWORK_NAME

# run mysql 5.7 docker
docker run --name $MY_SQL_DOCKER_NAME \
    -e MYSQL_ROOT_PASSWORD=$PASSWORD -p $MY_SQL_PORT:3306 \
    --net $MY_NETWORK_NAME -d mysql:5.7

# wait a bit for sql to set up
max_iter=10
mysql_running=false 
for i in `seq 2 $max_iter`
do
    RUNNING=$(docker inspect --format="{{.State.Running}}" $MY_SQL_DOCKER_NAME 2> /dev/null)
    if [ $? -eq 1 ]; then
        echo "UNKNOWN - $MY_SQL_DOCKER_NAME does not exist."
        exit 3
    fi

    if [ "$RUNNING" == "true" ]; then
        mysql_running=true
        break
    else
        echo "$MY_SQL_DOCKER_NAME is not running, sleep 1."
        sleep 1
    fi
done

# check if mysql is up
if [ "$mysql_running" = false ]; then
    exit 3
fi

# check connection for mysql
until nc -z -v -w30 0.0.0.0 $MY_SQL_PORT
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

# generate the envfile for server
echo DB_URI=mysql+pymysql://root:$PASSWORD@$MY_SQL_DOCKER_NAME:3306/picture?charset=utf8 > dev.env
echo ECRET_KEY=$MY_SERVER_SECRET_KEY >> dev.env

# build the server docker
make build
make run env=dev.env net-name=$MY_NETWORK_NAME