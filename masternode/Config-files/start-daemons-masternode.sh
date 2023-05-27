#!/bin/bash

HADOOP_HOME=/opt/bd/hadoop/
#Namenode
HDFS_SERVICE=${HADOOP_HOME}/bin/hdfs
NAMENODE_DAEMON=namenode

#Resource Manager
YARN_SERVICE=${HADOOP_HOME}/bin/yarn
RESOURCE_MANAGER_DAEMON=resourcemanager


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

# Espera un poco mas antes de crear directorios
sleep 5

# Inicia directorios en HDFS
#$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/hdadmin &&\
#$HADOOP_HOME/bin/hdfs dfs -mkdir -p /tmp/hadoop-yarn/staging &&\
#$HADOOP_HOME/bin/hdfs dfs -chmod -R 1777 /tmp

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
