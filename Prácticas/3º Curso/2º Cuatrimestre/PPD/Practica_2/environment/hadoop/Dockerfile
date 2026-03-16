# syntax=docker/dockerfile:1
ARG HADOOP_VERSION=3.3.6
FROM eclipse-temurin:11-jdk-jammy

ARG HADOOP_VERSION
ARG SPARK_VERSION=3.5.5
ARG TARGETARCH

ENV DEBIAN_FRONTEND=noninteractive
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH=$PATH:/opt/hadoop/bin:/opt/hadoop/sbin:/opt/spark/bin:/opt/spark/sbin

RUN apt-get update && apt-get install -y --no-install-recommends \
      bash ca-certificates curl tini procps netcat-openbsd \
      openssh-client openssh-server sudo vim-tiny \
      maven \
      python3 python3-pip python3-venv \
      rpcbind nfs-common \

    && rm -rf /var/lib/apt/lists/*

# Librerias Python usadas en las practicas de P2 (MapReduce/PySpark auxiliares).
RUN python3 -m pip install --no-cache-dir \
      "mrjob>=0.7.4" \
      "pyarrow>=14.0.0" \
      "pyspark==${SPARK_VERSION}"

# Descargar Hadoop (es Java, el binario sirve para amd64 y arm64)
# Intentamos primero downloads.apache.org y si falla, hacemos fallback a archive.apache.org.
RUN set -eux; \
    tgz="hadoop-${HADOOP_VERSION}.tar.gz"; \
    url1="https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/${tgz}"; \
    url2="https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/${tgz}"; \
    curl -fSL "${url1}" -o /tmp/hadoop.tgz || curl -fSL "${url2}" -o /tmp/hadoop.tgz; \
    tar -xzf /tmp/hadoop.tgz -C /opt; \
    mv "/opt/hadoop-${HADOOP_VERSION}" "${HADOOP_HOME}"; \
    rm -f /tmp/hadoop.tgz; \
    # directorios básicos
    mkdir -p /data/hdfs/namenode /data/hdfs/datanode /data/tmp /data/yarn/local /data/yarn/log; \
    mkdir -p /var/run/sshd

# Instalar Spark standalone para comandos spark-submit/spark-shell en workbench.
RUN set -eux; \
    spark_pkg="spark-${SPARK_VERSION}-bin-hadoop3"; \
    tgz="${spark_pkg}.tgz"; \
    url1="https://downloads.apache.org/spark/spark-${SPARK_VERSION}/${tgz}"; \
    url2="https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/${tgz}"; \
    curl -fSL "${url1}" -o /tmp/spark.tgz || curl -fSL "${url2}" -o /tmp/spark.tgz; \
    tar -xzf /tmp/spark.tgz -C /opt; \
    mv "/opt/${spark_pkg}" "${SPARK_HOME}"; \
    rm -f /tmp/spark.tgz

# Usuarios (usaremos los nombres de la práctica: hdadmin y luser)
RUN groupadd -r hadoop && \
    useradd -m -s /bin/bash -g hadoop hdadmin && \
    useradd -m -s /bin/bash -g hadoop luser && \
    echo "luser:luser" | chpasswd && \
    echo "hdadmin ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/hdadmin && \
    echo "luser ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/luser && \
    chmod 0440 /etc/sudoers.d/hdadmin /etc/sudoers.d/luser

# Hadoop env
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_CONF_DIR}/hadoop-env.sh && \
    echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_CONF_DIR}/yarn-env.sh && \
    echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_CONF_DIR}/mapred-env.sh && \
    printf '%s\n' \
      'export HADOOP_HOME=/opt/hadoop' \
      'export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop' \
      'export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' \
      > /etc/profile.d/hadoop.sh

COPY conf/ ${HADOOP_CONF_DIR}/
COPY scripts/ /opt/hadoop-lab/
RUN chmod +x /opt/hadoop-lab/*.sh

ENTRYPOINT ["/usr/bin/tini","--","/opt/hadoop-lab/entrypoint.sh"]
