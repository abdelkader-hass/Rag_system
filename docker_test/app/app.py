from flask import Flask, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Connect to local Neo4j (running in same container)
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "adminneo4j"))

@app.route("/")
def index():
    with driver.session() as session:
        result = session.run("RETURN 'Hello from Neo4j!' AS msg")
        msg = result.single()["msg"]
        return jsonify({"message": msg})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
