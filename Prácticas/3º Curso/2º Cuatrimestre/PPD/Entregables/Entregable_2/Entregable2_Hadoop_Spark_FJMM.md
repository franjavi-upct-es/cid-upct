---
title: "Procesamiento Paralelo de Datos"
subtitle: "Tarea 2: Hadoop MapReduce y Apache Spark"
author: "Francisco Javier Mercader Martínez"
lang: es
format:
  pdf:
    documentclass: article
    listings: true
    toc: true
    toc-title: "Índice"
    number-sections: true
    colorlinks: true
    include-in-header:
      text: |
        \usepackage[table]{xcolor}
        \usepackage{listings}
        \usepackage{enumitem}
        \usepackage{multicol}
        \usepackage{graphicx}
        \usepackage{float}
        \usepackage{tikz} 
        \lstset{
          language=Python,
          basicstyle=\ttfamily\small,
          numberstyle=\tiny,
          keywordstyle=\color{blue},
          commentstyle=\color{olive},
          stringstyle=\color{red},
          breakatwhitespace=false, 
          breaklines=true,
          showspaces=false,
          showstringspaces=false,
          showtabs=false, 
          tabsize=2,
          literate={á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1{ñ}{{\~n}}1 {Á}{{\'A}}1 {Í}{{\'I}}1 {Ú}{{\'U}}1 {¿}{{\textexclamdown}}1,
          mathescape=false,
          backgroundcolor=\color{lightgray!10}
        }
        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \fancyhf{}
        \fancyhead[R]{\textit{Procesamiento Paralelo de Datos}}
        \fancyfoot[C]{\thepage}
linestrectch: 1.5
fontisize: 12
papersize: a4
geometry: margin=1.5cm
execute:
  echo: false
  warning: false
---

\newpage

# Manejo de un clúster Hadoop 3. Gestión HDFS y YARN
## Inicio del clúster Hadoop con contenedores Docker ##

```bash
pyros05@Pyros-Nitro-ANV15-52:~/p2$ ./start.sh 
[+] up 7/7
 ✔ Container namenode      Healthy                                                                                                                                                        0.5s
 ✔ Container nfsgateway    Running                                                                                                                                                        0.0s
 ✔ Container datanode2     Running                                                                                                                                                        0.0s
 ✔ Container workbench     Running                                                                                                                                                        0.0s
 ✔ Container datanode3     Running                                                                                                                                                        0.0s
 ✔ Container historyserver Running                                                                                                                                                        0.0s
 ✔ Container datanode1     Running     
```

Ejecución de los contenedores Docker que contienen cada uno de los nodos del clúster.

```bash
pyros05@Pyros-Nitro-ANV15-52:~/p2$ docker compose ps
NAME            IMAGE              COMMAND                  SERVICE         CREATED         STATUS                   PORTS
datanode1       hadoop-lab:3.3.6   "/usr/bin/tini -- /o…"   datanode1       5 minutes ago   Up 5 minutes             
datanode2       hadoop-lab:3.3.6   "/usr/bin/tini -- /o…"   datanode2       5 minutes ago   Up 5 minutes             
datanode3       hadoop-lab:3.3.6   "/usr/bin/tini -- /o…"   datanode3       5 minutes ago   Up 5 minutes             
historyserver   hadoop-lab:3.3.6   "/usr/bin/tini -- /o…"   historyserver   5 minutes ago   Up 5 minutes             0.0.0.0:19888->19888/tcp, [::]:19888->19888/tcp
namenode        hadoop-lab:3.3.6   "/usr/bin/tini -- /o…"   namenode        5 minutes ago   Up 5 minutes (healthy)   0.0.0.0:8088->8088/tcp, [::]:8088->8088/tcp, 0.0.0.0:9000->9000/tcp, [::]:9000->9000/tcp, 0.0.0.0:9870->9870/tcp, [::]:9870->9870/tcp
nfsgateway      hadoop-lab:3.3.6   "/usr/bin/tini -- /o…"   nfsgateway      5 minutes ago   Up 5 minutes             0.0.0.0:2049->2049/tcp, 0.0.0.0:2049->2049/udp, [::]:2049->2049/tcp, [::]:2049->2049/udp, 0.0.0.0:4242->4242/tcp, 0.0.0.0:4242->4242/udp, [::]:4242->4242/tcp, [::]:4242->4242/udp
workbench       hadoop-lab:3.3.6   "/usr/bin/tini -- /o…"   workbench       5 minutes ago   Up 5 minutes  
```

Comprobamos el estado correcto de los contenedores lanzados y abrimos una terminal bash en modo interactivo en el namenode.

```bash
pyros05@Pyros-Nitro-ANV15-52:~/p2$ sudo ./mount-hdfs.sh mount
Montando HDFS (vía NFS) en: /home/pyros05/hdfs
Export: /user/luser
Opciones NFS: nfsvers=3,proto=tcp,mountproto=tcp,port=2049,mountport=4242,nolock,noacl,hard,timeo=150,retrans=5
Necesitas nfs-common (Debian/Ubuntu) o nfs-utils (Fedora/RHEL).


OK. Prueba: ls -la /home/pyros05/hdfs
Para desmontar: mount-hdfs.sh umount
```

```bash
pyros05@Pyros-Nitro-ANV15-52:~/p2$ GET http://localhost:9870 | head -n 10
<!--
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

pyros05@Pyros-Nitro-ANV15-52:~/p2$ GET http://localhost:8088 | head -n 10
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <meta http-equiv="X-UA-Compatible" content="IE=8">
  <meta http-equiv="Content-type" content="text/html; charset=UTF-8">
  <style type="text/css">
    #apps_paginate span {font-weight:normal}
    #apps .progress {width:8em}
    #apps_processing {top:-1.5em; font-size:1em;
      color:#000; background:#fefefe}
    #apps .queue {width:6em}
pyros05@Pyros-Nitro-ANV15-52:~/p2$ GET http://localhost:19888 | head -n 10
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <meta http-equiv="X-UA-Compatible" content="IE=8">
  <meta http-equiv="Content-type" content="text/html; charset=UTF-8">
  <style type="text/css">
    #jobs_paginate span {font-weight:normal}
    #jobs .progress {width:8em}
    #jobs_processing {top:-1.5em; font-size:1em;
      color:#000; background:#fefefe}
  </style>
```

## Inicio del cluster Hadoop con contenedores Docker ##


