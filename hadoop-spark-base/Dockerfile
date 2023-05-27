FROM ubuntu:latest

# Switch to root user
USER root

ENV BASE_DIR /opt/bd
ENV LOG_TAG "[BASE Hadoop_${HADOOP_VERSION}_Spark_${SPARK_VERSION}]:"

#HADOOP VARS
ENV HADOOP_VERSION 3.3.1
ENV HADOOP_REPOSITORY https://dlcdn.apache.org/hadoop/common

#SPARK VARS
ENV SPARK_VERSION 3.4.0
ENV SPARK_REPOSITORY https://dlcdn.apache.org/spark

# STEP 1: Instala java y demas software necesario
RUN echo "$LOG_TAG Actualizando e instalando paquetes básicos" && \
    apt-get update && \
    apt-get install -y openjdk-8-jre python3 curl locales iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists

# Genera locales
#RUN echo "$LOG_TAG Creando locales" && \
 #   locale-gen es_ES.UTF-8 && update-locale LANG=es_ES.UTF-8

# Crea un directorio para la instalación en /opt: 
RUN mkdir -p ${BASE_DIR}
    
# Change to /opt/bd directory
WORKDIR ${BASE_DIR}

# Descarga la versión 3.1.1 Hadoop en /opt/bd y crea enlace simbolico a "hadoop"
RUN echo "$LOG_TAG Descargando Hadoop" && \
    curl -fLO "${HADOOP_REPOSITORY}/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz"  && \
    tar xzvf hadoop-${HADOOP_VERSION}.tar.gz && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Descarga la version 3.3.4 de Spark en /opt/bd y crea enlace simbolico a "spark"
RUN echo "${LOG_TAG} Descargando Spark" && \
	curl -fLO "${SPARK_REPOSITORY}/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-without-hadoop.tgz"  && \
    tar xzvf spark-${SPARK_VERSION}-bin-without-hadoop.tgz && \
    ln -s spark-${SPARK_VERSION}-bin-without-hadoop spark && \
    rm spark-${SPARK_VERSION}-bin-without-hadoop.tgz


# ENV VARS
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

#HADOOP AND YARN ENV VARS
ENV HADOOP_HOME ${BASE_DIR}/hadoop/
ENV HADOOP_CONF_DIR ${HADOOP_HOME}/etc/hadoop/
#ENV YARN_CONF_DIR ${HADOOP_HOME}/etc/hadoop/ --> ha sido reemplazado por hadoop_conf_dir
ENV DATA_DIR /var/data/hadoop/hdfs
ENV PATH ${PATH}:${HADOOP_HOME}/bin/:${HADOOP_HOME}/sbin/


#SPARK_ENV_VARS
ENV SPARK_HOME=${BASE_DIR}/spark/
ENV SPARK_CONF_DIR=${SPARK_HOME}/
ENV PATH=$PATH:$SPARK_HOME/bin

# Copia ficheros de configuracion de spark
COPY spark-config-files/spark-env.sh ${SPARK_CONF_DIR}/spark-env.sh
COPY spark-config-files/log4j2.properties ${SPARK_CONF_DIR}/log4j2.properties

