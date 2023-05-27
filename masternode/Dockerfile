FROM hadoop-spark-image:latest

# Dockerfile para el NameNode
# Switch to root user
USER root

# Define valores de entorno
ENV HADOOP_VERSION 3.3.1
ENV LOG_TAG "[Masternode]:"
ENV BASE_DIR /opt/bd
ENV HADOOP_HOME ${BASE_DIR}/hadoop/
ENV HADOOP_CONF_DIR ${HADOOP_HOME}/etc/hadoop/
ENV DATA_DIR /var/data/hadoop/hdfs


# Crea directorios para los datos de HDFS del NameNode
# En un sistema real, deberíamos crear varios directorios en particiones separadas con suficiente espacio libre.
RUN echo "$LOG_TAG Crea directorios para los datos de HDFS del NameNode" && \
    mkdir -p ${DATA_DIR}/nn

# Crea directorio para los ficheros de log
RUN echo "$LOG_TAG Crea directorio para los ficheros de log" && \
    mkdir ${HADOOP_HOME}/logs

# Copia los ficheros de configuracion
RUN echo "$LOG_TAG Copia los ficheros de configuracion y el script de inicio"
COPY Config-files/core-site.xml ${HADOOP_CONF_DIR}/core-site.xml
COPY Config-files/hdfs-site-namenode.xml ${HADOOP_CONF_DIR}/hdfs-site.xml
COPY Config-files/yarn-site-resourcemanager.xml ${HADOOP_CONF_DIR}/yarn-site.xml
COPY Config-files/mapred-site-resourcemanager.xml ${HADOOP_CONF_DIR}/mapred-site.xml

# Script de inicio 
COPY Config-files/start-daemons-masternode.sh ${BASE_DIR}/start-daemons.sh

# Establece permisos de ejecución
RUN chmod +x ${BASE_DIR}/start-daemons.sh

# Expose Namenode ports 
EXPOSE 8020 9820 9870 9871

# Expose ResourceManager ports
EXPOSE 8030 8031 8032 8033 8088 8090  

# Expose Spark Ports
EXPOSE 4040

WORKDIR ${HADOOP_HOME}

RUN echo "$LOG_TAG Iniciando demonios"
CMD ["/opt/bd/start-daemons.sh"]
