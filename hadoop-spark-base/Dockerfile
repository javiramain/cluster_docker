FROM ubuntu:20.04

USER root

ENV BASE_DIR /opt/bd
ENV LOG_TAG "[BASE Hadoop_${HADOOP_VERSION}_Spark_${SPARK_VERSION}]:"

#HADOOP VARS
ENV HADOOP_VERSION 3.3.5
ENV HADOOP_REPOSITORY https://dlcdn.apache.org/hadoop/common

#SPARK VARS
ENV SPARK_VERSION 3.3.1
ENV SPARK_REPOSITORY https://archive.apache.org/dist/spark

#KAKFA_VARS
ENV KAFKA_VERSION 2.12-2.8.1
ENV KAFKA_SHORT_VERSION 2.8.1
ENV KAFKA_REPOSITORY https://archive.apache.org/dist/kafka

# STEP 1: Instala java y demas software necesario. Quitar lo que ya no es necesario
RUN echo "$LOG_TAG Actualizando e instalando paquetes básicos" && \
    apt-get update && \
    apt-get install -y openjdk-8-jre python3 curl locales nano systemd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists

# Genera locales
RUN echo "$LOG_TAG Creando locales" && \
    locale-gen es_ES.UTF-8 && update-locale LANG=es_ES.UTF-8

# Crea un directorio para la instalación en /opt: 
RUN mkdir -p ${BASE_DIR}
    
# Change to /opt/bd directory
WORKDIR ${BASE_DIR}

#DESCARGAS:
RUN apt-get update && apt-get install -y python3-pip

# Descarga la versión 3.3.5 de Hadoop en /opt/bd y crea enlace simbolico a "hadoop"
RUN echo "$LOG_TAG Descargando Hadoop" && \
    curl -fLO "${HADOOP_REPOSITORY}/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz"  && \
    tar xzvf hadoop-${HADOOP_VERSION}.tar.gz && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Descarga la version 3.4.0 de Spark en /opt/bd y crea enlace simbolico a "spark"
RUN echo "${LOG_TAG} Descargando Spark" && \
	curl -fLO "${SPARK_REPOSITORY}/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-without-hadoop.tgz"  && \
    tar xzvf spark-${SPARK_VERSION}-bin-without-hadoop.tgz && \
    ln -s spark-${SPARK_VERSION}-bin-without-hadoop spark && \
    rm spark-${SPARK_VERSION}-bin-without-hadoop.tgz

# Descarga la version 2.8.1 de Kafka en /opt/bd y crea enlace simbolico a "kafka":
RUN echo "${LOG_TAG} Descargando Kakfa" && \
	curl -fLO "${KAFKA_REPOSITORY}/${KAFKA_SHORT_VERSION}/kafka_${KAFKA_VERSION}.tgz" && \
	tar xzvf kafka_${KAFKA_VERSION}.tgz && \
    ln -s kafka_${KAFKA_VERSION} kafka && \
    rm kafka_${KAFKA_VERSION}.tgz

# Descarga la version 5.0.16 de MongoDb a traves del gestor de paquetes apt. Instala libssl1.1, necesario para la instalacion de mongo en ubuntu 22.04
RUN echo "${LOG_TAG} Descargando MongoDB" && \
    apt-get update && \
    apt-get install -y gnupg && \
    curl https://pgp.mongodb.com/server-4.4.asc | \
    gpg -o /usr/share/keyrings/mongodb-server-4.4.gpg \
    --dearmor && \
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-4.4.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list && \
	apt-get update && \
    apt-get install -y mongodb-org=4.4.22 mongodb-org-server=4.4.22 mongodb-org-shell=4.4.22 mongodb-org-mongos=4.4.22 mongodb-org-tools=4.4.22


# Fijar la version de los paquetes para que Mongo no se acutalice de forma automatica 
RUN echo "mongodb-org hold" | dpkg --set-selections && \
echo "mongodb-org-database hold" | dpkg --set-selections && \
echo "mongodb-org-server hold" | dpkg --set-selections && \
echo "mongodb-org-shell hold" | dpkg --set-selections  && \
echo "mongodb-org-mongos hold" | dpkg --set-selections  && \
echo "mongodb-org-tools hold" | dpkg --set-selections
	
# ENV VARS
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV PATH ${PATH}:${JAVA_HOME}/bin
ENV PATH ${PATH}:/usr/bin/systemctl
#KAFKA ENV VARS
ENV KAFKA_HOME=${BASE_DIR}/kafka
ENV PATH=${PATH}:${KAFKA_HOME}/bin


#HADOOP AND YARN ENV VARS
ENV HADOOP_HOME ${BASE_DIR}/hadoop
ENV HADOOP_CONF_DIR ${HADOOP_HOME}/etc/hadoop/


#ENV YARN_CONF_DIR ${HADOOP_HOME}/etc/hadoop/ --> ha sido reemplazado por hadoop_conf_dir
ENV DATA_DIR /var/data/hadoop/hdfs
ENV PATH ${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin/

#SPARK_ENV_VARS
ENV SPARK_HOME=${BASE_DIR}/spark
#ENV SPARK_CONF_DIR=${SPARK_HOME}/
ENV SPARK_CONF_DIR=${SPARK_HOME}/conf  
ENV PATH=${PATH}:${SPARK_HOME}/bin

#KAFKA ENV VARS
#ENV KAFKA_HOME=${BASE_DIR}/kafka/
#ENV PATH=$PATH:$KAFKA_HOME/bin


# Copia ficheros de configuracion de spark
COPY spark-config-files/spark-env.sh ${SPARK_CONF_DIR}/spark-env.sh
COPY spark-config-files/log4j2.properties ${SPARK_CONF_DIR}/log4j2.properties

