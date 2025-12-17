from flask import Flask, request, jsonify
from ai import generate_study_plan

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return {"status": "Backend is running"}, 200

@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    try:
        data = request.get_json()

        required_fields = ["subject", "exam_date", "hours", "study_mode"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        plan = generate_study_plan(
            data["subject"],
            data["exam_date"],
            data["hours"],
            data["study_mode"]
        )

        return jsonify(plan)

    except Exception as e:
        print("BACKEND ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
