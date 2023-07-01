#!/bin/bash

HADOOP_HOME=/opt/bd/hadoop/

SERVICE1=${HADOOP_HOME}/bin/hdfs
DAEMON1=datanode

SERVICE2=${HADOOP_HOME}/bin/yarn
DAEMON2=nodemanager



# Iniciamos el demonio del DataNode y chequeamos si ha arrancado
 ${SERVICE1} --daemon start ${DAEMON1}
status=$?
if [ $status -ne 0 ]; then
  echo "No pudo inicializar el servicio ${DAEMON1}: $status"
  exit $status
fi

# Iniciamos el demonio del NodeManager y chequeamos si ha arrancado
 ${SERVICE2} --daemon start ${DAEMON2}
status=$?
if [ $status -ne 0 ]; then
  echo "No pudo inicializar el servicio ${DAEMON2}: $status"
  exit $status
fi

# Se asigna a cada workernode del cluster un puerto para el servicio de mongoDB
if [[ "$HOSTNAME" = "workernode1" ]];  then 
    puerto="27019"
elif [[ "$HOSTNAME" = "workernode2" ]]; then 
    puerto="27020"
elif [[ "$HOSTNAME" = "workernode3" ]]; then 
    puerto="27021"
fi

echo "para el $HOSTNAME se asigna el puerto $puerto"

# Se crean los directorios de datos necesarios en las rutas que serviran de volumen
mkdir -p /home/mongo/db/

#Arrancamos el servicio de mongoDB
mongod --port 27017 --bind_ip_all --dbpath /home/mongo/db --replSet mongodbReplicaSet 

#Arrancamos brokers de kafka, esperando a que el servicio de zookeeper este activo:
sleep 5
kafka-server-start.sh ${KAFKA_HOME}/config/$(hostname).server.properties &


# Mientras ambos demonio estén vivos, el contenedor sigue activo
while true
do 
  sleep 10
  if ! ps aux | grep ${DAEMON1} | grep -q -v grep
  then
     echo "El demonio ${DAEMON1}  ha fallado"
      exit 1
  fi
  if ! ps aux | grep ${DAEMON2} | grep -q -v grep
  then
      echo "El demonio ${DAEMON2}  ha fallado"
      exit 1
  fi
done
