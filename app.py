from flask import Flask, render_template, request
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# counters
user_count = 0
valid_count = 0
invalid_count = 0


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/verify", methods=["POST"])
def verify():
    global user_count, valid_count, invalid_count

    document = request.files["document"]
    signature = request.files["signature"]

    doc_path = os.path.join(app.config["UPLOAD_FOLDER"], document.filename)
    sig_path = os.path.join(app.config["UPLOAD_FOLDER"], signature.filename)

    document.save(doc_path)
    signature.save(sig_path)

    try:
        with open(doc_path, "rb") as f:
            data = f.read()

        with open(sig_path, "rb") as f:
            sig = f.read()

        # load server public key
        with open("public_key.pem", "rb") as f:
            public_key = load_pem_public_key(f.read())

        # verify signature
        public_key.verify(
            sig,
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        verification_success = True

    except Exception as e:
        print("Verification error:", e)
        verification_success = False

    user_count += 1

    if verification_success:
        valid_count += 1
        return render_template("index.html", result="valid", users=user_count)

    else:
        invalid_count += 1
        return render_template("index.html", result="invalid", users=user_count)


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        users=user_count,
        valid=valid_count,
        invalid=invalid_count
    )


if __name__ == "__main__":
    app.run(debug=True)