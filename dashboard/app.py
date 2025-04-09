from flask import Flask, jsonify, render_template
import boto3
from boto3.dynamodb.conditions import Key
import os

app = Flask(__name__)

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table_name = os.getenv("DYNAMO_TABLE", "CloudHunterThreatLogs")
table = dynamodb.Table(table_name)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/events")
def get_events():
    try:
        response = table.scan(Limit=10)
        items = response.get("Items", [])
        return jsonify({"events": items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5001, debug=True)
