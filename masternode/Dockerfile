FROM hadoop-spark-image:2.0.0

# Dockerfile para el NameNode
# Switch to root user
USER root

# Define valores de entorno
ENV LOG_TAG "[Masternode]:"
ENV BASE_DIR /opt/bd

ENV DATA_DIR /var/data/hadoop/hdfs
ENV HOME_DIR /home

#KAFKA ENV VARS
#ENV KAFKA_HOME=${BASE_DIR}/kafka
#ENV PATH=$PATH:$KAFKA_HOME/bin

# Crea directorios para los datos de HDFS del NameNode
# En un sistema real, deberíamos crear varios directorios en particiones separadas con suficiente espacio libre.
RUN echo "$LOG_TAG Crea directorios para los datos de HDFS del NameNode" && \
    mkdir -p ${DATA_DIR}/nn

# Crea directorio para los ficheros de log
RUN echo "$LOG_TAG Crea directorio para los ficheros de log" && \
    mkdir ${HADOOP_HOME}/logs


# Copia los ficheros de configuracion de hadoop, hdfs, yarn y mapReduce
RUN echo "$LOG_TAG Copia los ficheros de configuracion y el script de inicio"
COPY Config-files/core-site.xml ${HADOOP_CONF_DIR}/core-site.xml
COPY Config-files/hdfs-site-namenode.xml ${HADOOP_CONF_DIR}/hdfs-site.xml
COPY Config-files/yarn-site-resourcemanager.xml ${HADOOP_CONF_DIR}/yarn-site.xml
COPY Config-files/mapred-site-resourcemanager.xml ${HADOOP_CONF_DIR}/mapred-site.xml
COPY Config-files/capacity-scheduler.xml ${HADOOP_CONF_DIR}/capacity-scheduler.xml

# Copia los el fichero de configuracion de zookeeper
COPY Config-files/zookeeper.properties ${KAFKA_HOME}/config/zookeeper.properties

#Copia el fichero de configuracion del servicio de mongodb
COPY Config-files/mongod.conf /etc/mongod.conf

#Copia los scripts de streamlit y la carpeta donde se depositan temporalmente los ficheros
COPY streamlit/ /streamlit
#COPY streamlit/pages/carga_datos.py /streamlit/pages

# Copia los scripts de arranque de spark y hdfs
COPY scripts /scripts


# Copia el script de inicio de todos los servicios
COPY scripts/start-services-masternode.sh ${BASE_DIR}/start-services.sh

# Instala paquetes de streamlit y kafka-python para el producer y el consumer de la webapp
RUN yes | pip install streamlit
RUN yes | pip install kafka-python

# Establece permisos de ejecución
RUN chmod +x ${BASE_DIR}/start-services.sh

#RUN zookeeper-server-start.sh ${KAFKA_HOME}/config/zookeeper.properties &&
#RUN kafka-server-start.sh ${KAFKA_HOME}/config/server.properties &


# Expose Namenode ports 
EXPOSE 8020 9820 9870 9871

# Expose ResourceManager ports
EXPOSE 8030 8031 8032 8033 8088 8090  
# YARN LOGs
EXPOSE 8034

# Expose Spark Ports (from 4040 onward for each sparkContext)
EXPOSE 4040-4045 8080 

# Expose zookeeper port
EXPOSE 2181 9092

# Expose mongo default and aditional port
EXPOSE 27017-27027

# Expose streamlit port so you can access it from your local web browser
EXPOSE 8501 

WORKDIR ${HOME_DIR}

RUN echo "$LOG_TAG Iniciando demonios"
CMD ["/opt/bd/start-services.sh"]
