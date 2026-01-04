from flask import Flask, jsonify, request
from function.node_service import NodeService

# ubah True kalau ingin debug
DEBUG = False

app = Flask(__name__)

node_service = NodeService()


@app.route("/api/read/node", methods=["GET"])
def read_node():
    try:
        rows = node_service.readNode()

        data = []
        for row in rows:
            data.append({
                "node_id": row["id"],
                "name": row["name"],
                "total_sensor": 0,
                "updated_at": row["updated_at"]
            })
        
        if(DEBUG):
            print("Data node :")
            print(data)

        message = "Berhasil mengambil data node"
        if len(data) == 0:
            message = "Data node masih kosong"

        result = jsonify({
            "status": "Success",
            "message": message,
            "data": data
        })
        return result

    except Exception as e:
        if(DEBUG):
            print("Error mengambil data node : ", e)

        return jsonify({
            "status": "Failed",
            "message": str(e),
            "data": []
        }), 500


@app.route("/api/create/node", methods=["POST"])
def create_node():
    try:
        body = request.get_json()
        name = body.get("name")

        node_service.createNode(name)

        rows = node_service.readNode()
        data = []
        for row in rows:
            data.append({
                "node_id": row["id"],
                "name": row["name"],
                "total_sensor": 0,
                "updated_at": row["updated_at"]
            })

        return jsonify({
            "status": "Success",
            "message": "Data node berhasil ditambahkan",
            "data": data
        })

    except Exception as e:
        print("Error menambah data node")
        return jsonify({
            "status": "Failed",
            "message": str(e),
            "data": []
        }), 400
    

@app.route("/api/update/node", methods=["POST"])
def update_node():
    try:
        body = request.get_json()
        node_id = body.get("node_id")
        name = body.get("name")

        node_service.updateNode(node_id, name)

        rows = node_service.readNode()
        data = []
        for row in rows:
            data.append({
                "node_id": row["id"],
                "name": row["name"],
                "total_sensor": 0,
                "updated_at": row["updated_at"]
            })

        return jsonify({
            "status": "Success",
            "message": "Data node berhasil diupdate",
            "data": data
        })

    except Exception as e:
        if(DEBUG):
            print("Error mengupdate data node : ", e)

        return jsonify({
            "status": "Failed",
            "message": str(e),
            "data": []
        }), 400
    

@app.route("/api/delete/node", methods=["POST"])
def delete_node():
    try:
        body = request.get_json()
        node_id = body.get("node_id")

        node_service.deleteNode(node_id)

        rows = node_service.readNode()
        data = []
        for row in rows:
            data.append({
                "node_id": row["id"],
                "name": row["name"],
                "total_sensor": 0,
                "updated_at": row["updated_at"]
            })

        return jsonify({
            "status": "Success",
            "message": "Data node berhasil dihapus",
            "data": data
        })

    except Exception as e:
        if(DEBUG):
            print("Error menghapus data node : ", e)

        return jsonify({
            "status": "Failed",
            "message": str(e),
            "data": []
        }), 400

    

if __name__ == "__main__":
    app.run(port=8081, debug=True)
