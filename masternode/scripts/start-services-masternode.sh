#!/bin/bash

#HADOOP_HOME=/opt/bd/hadoop/
#Namenode
HDFS_SERVICE=${HADOOP_HOME}/bin/hdfs
NAMENODE_DAEMON=namenode

#Resource Manager
YARN_SERVICE=${HADOOP_HOME}/bin/yarn
RESOURCE_MANAGER_DAEMON=resourcemanager

#Spark
SPARK_MASTER_SERVICE=${SPARK_HOME}/

# Formateamos el NameNode en modo no interactivo
# si existen datos, no se reformatea
$HADOOP_HOME/bin/hdfs namenode -format -nonInteractive 2> /dev/null

# Iniciamos el demonio del namenode y chequeamos si ha arrancado
${HDFS_SERVICE} --daemon start ${NAMENODE_DAEMON}
status=$?
if [ $status -ne 0 ]; then
  echo "No pudo inicializar el servicio ${NAMENODE_DAEMON}: $status"
  exit $status
fi


# Iniciamos el demonio del resourcemanager y chequeamos si ha arrancado
${YARN_SERVICE} --daemon start ${RESOURCE_MANAGER_DAEMON}
status=$?
if [ $status -ne 0 ]; then
  echo "No pudo inicializar el servicio ${RESOURCE_MANAGER}: $status"
  exit $status
fi

# Esperamos a que el demonio este iniciado
while ! ps aux | grep ${NAMENODE_DAEMON} | grep -q -v grep
do 
    sleep 1 
done

# Se crean los directorios de datos necesarios en las rutas que serviran de volumen si no existen
mkdir -p /home/zookeeper/data && mkdir -p /home/mongo/db

# Se copian los scripts de ejecucion y de streamlit
cp -r /streamlit /home && cp -r /scripts /home

#Arrancamos en segundo plano el servicio de mongoDB
mongod --config /etc/mongod.conf --bind_ip_all &
# Comprobamos si el replicaSet ha sido arrancado previamente. Si no, se inicia, se configura y se añaden unos datos
# iniciales de muestra. Si el rs.status() devuelve el codigo 94, no ha sido inicializado.
sleep 3
echo "Comprobando el estado del replicaSet"
init_status=$(mongo --eval "rs.status().code")

if [ "${init_status: -2}" = "94" ]; then
    echo "Mongo ReplicaSet is not initialized. Initializing....."
    mongo < /home/scripts/start-replicaSet.js
    echo "Mongo Replica Set is ready!"
fi

#Arranca en segundo plano el servicio de zookeeper
zookeeper-server-start.sh ${KAFKA_HOME}/config/zookeeper.properties &

#Esperamos a que zookeeper este levantado y los workers levanten el servicio de kafka,
# y se crea el topic que servirá para trasladar la consulta al Streaming
sleep 3
kafka-topics.sh --create --topic streaming-query --bootstrap-server workernode1:9092
kafka-topics.sh --create --topic output --bootstrap-server workernode1:9092

# Arrancar el streaming
sh /home/scripts/run-spark-streaming.sh &

# Arrancar la web-app
streamlit run /home/streamlit/busqueda.py &


# Mientras el demonio esté vivo, el contenedor sigue activo
while true
do 
  sleep 10
  if ! ps aux | grep ${NAMENODE_DAEMON} | grep -q -v grep
  then
      echo "El demonio ${NAMENODE_DAEMON}  ha fallado"
      exit 1
  fi
  if ! ps aux | grep ${RESOURCE_MANAGER_DAEMON} | grep -q -v grep
  then
      echo "El demonio ${RESOURCE_MANAGER_DAEMON}  ha fallado"
      exit 1
  fi
done
