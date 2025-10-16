# Start from official Neo4j image (includes Java)
FROM neo4j:community

# Install Python and pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Flask app
COPY app/ /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose Flask port (5000) and Neo4j ports
EXPOSE 5000 7474 7687

# Set Neo4j auth (optional)
# ENV NEO4J_AUTH=neo4j/test123

# Start Neo4j and Flask
CMD ["bash", "-c", "neo4j start && python3 app.py"]


#docker run -p 5000:5000 -p 7474:7474 -p 7687:7687 -v /home/grigoriev_adm/AI/dev/chroma_db_server/volume_test:/data  imagetestneo4j:latest
# docker run   -p 5009:5009 -p 7474:7474 -p 7687:7687  /
#  -v /home/grigoriev_adm/AI/dev/chroma_db_server/volume_test/sav_palaiseau1:/data /
#    -e MAIN_FOLDER=data   graphrag_neo4j:latest