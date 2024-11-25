FROM openjdk:11

# Provide the name of the GraphDB ZIP file during build
ARG GRAPHDB_ZIP=graphdb-10.6.1-dist.zip

# Ensure the ZIP file is provided
RUN : "${GRAPHDB_ZIP:?Build argument GRAPHDB_ZIP not provided}"

ENV GRAPHDB_VOLUME=/graphdb
ENV GRAPHDB_HOME=${GRAPHDB_VOLUME}/home
ENV GRAPHDB_INSTALL_DIR=${GRAPHDB_VOLUME}/dist
RUN mkdir -p $GRAPHDB_HOME $GRAPHDB_INSTALL_DIR

# Add the GraphDB distribution ZIP file to the container
ADD $GRAPHDB_ZIP /tmp/

WORKDIR /tmp
# Unzip the GraphDB ZIP, find the GraphDB directory, and move its contents to the install directory
RUN unzip -q $GRAPHDB_ZIP && \
    GRAPHDB_DIR=$(ls -d graphdb-*/) && \
    mv ${GRAPHDB_DIR}* $GRAPHDB_INSTALL_DIR && \
    rm -f $GRAPHDB_ZIP

# Ensure the graphdb script is executable
RUN chmod +x $GRAPHDB_INSTALL_DIR/bin/graphdb

ENV PATH=$GRAPHDB_INSTALL_DIR/bin:$PATH

VOLUME $GRAPHDB_VOLUME

EXPOSE 7200

# Adjust the CMD to provide default GraphDB flags or configurations
CMD ["-Dgraphdb.home=/graphdb/home", "-Dgraphdb.logback=conf/logback.xml"]

# Correctly set the ENTRYPOINT to the GraphDB executable
ENTRYPOINT ["graphdb"]
