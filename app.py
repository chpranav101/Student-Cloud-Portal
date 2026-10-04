from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import boto3
from botocore.config import Config
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "student-cloud-secret-key"

DATABASE = "database.db"

# AWS S3
S3_BUCKET = "student-cloud-portal-files-2026"
s3 = boto3.client(
    "s3",
    region_name="ap-south-1",
    config=Config(signature_version="s3v4")
)


# ================= DATABASE =================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    # Student information
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            year TEXT NOT NULL
        )
    """)

    # Login users
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student'
        )
    """)

    conn.commit()

    # Create default admin account
    admin = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        ("admin@studentcloud.com",)
    ).fetchone()

    if not admin:
        hashed_password = generate_password_hash("admin123")

        conn.execute(
            """
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                "Administrator",
                "admin@studentcloud.com",
                hashed_password,
                "admin"
            )
        )

        conn.commit()

    conn.close()


# ================= HOME =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= STUDENT REGISTRATION =================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        course = request.form.get("course")
        year = request.form.get("year")

        # Validation
        if not name or not email or not password or not course or not year:
            return render_template(
                "register.html",
                error="All fields are required."
            )

        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        if len(password) < 6:
            return render_template(
                "register.html",
                error="Password must contain at least 6 characters."
            )

        conn = get_db_connection()

        # Check existing account
        existing_user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if existing_user:
            conn.close()

            return render_template(
                "register.html",
                error="Email is already registered."
            )

        # Create hashed password
        hashed_password = generate_password_hash(password)

        # Create user account
        conn.execute(
            """
            INSERT INTO users
            (name, email, password, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email,
                hashed_password,
                "student"
            )
        )

        # Create student record automatically
        conn.execute(
            """
            INSERT INTO students
            (name, email, course, year)
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email,
                course,
                year
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session.clear()

            session["logged_in"] = True
            session["user_id"] = user["id"]
            session["username"] = user["name"]
            session["email"] = user["email"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))

            return redirect(url_for("student_dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


# ================= ADMIN DASHBOARD =================

@app.route("/admin")
def admin_dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return redirect(url_for("student_dashboard"))

    conn = get_db_connection()

    student_count = conn.execute(
        "SELECT COUNT(*) AS count FROM students"
    ).fetchone()["count"]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        student_count=student_count
    )


# ================= STUDENT DASHBOARD =================

@app.route("/student-dashboard")
def student_dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("role") != "student":
        return redirect(url_for("admin_dashboard"))

    return render_template(
        "student_dashboard.html"
    )


# ================= VIEW STUDENTS =================

@app.route("/students")
def students():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return redirect(url_for("student_dashboard"))

    conn = get_db_connection()

    students = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students
    )


# ================= STUDENT DOCUMENT UPLOAD =================

@app.route("/upload-document", methods=["GET", "POST"])
def upload_document():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("role") != "student":
        return redirect(url_for("admin_documents"))

    if request.method == "POST":

        file = request.files.get("document")

        if not file or file.filename == "":
            return render_template(
                "upload_document.html",
                error="Please select a file."
            )

        try:

            user_id = session.get("user_id")

            filename = f"student_{user_id}_{file.filename}"

            s3.upload_fileobj(
                file,
                S3_BUCKET,
                filename
            )

            return render_template(
                "upload_document.html",
                success="Document uploaded successfully to Amazon S3."
            )

        except Exception as e:

            return render_template(
                "upload_document.html",
                error=f"Upload failed: {str(e)}"
            )

    return render_template(
        "upload_document.html"
    )


# ================= ADMIN DOCUMENTS =================

@app.route("/admin/documents")
def admin_documents():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return redirect(url_for("student_dashboard"))

    try:

        response = s3.list_objects_v2(
            Bucket=S3_BUCKET
        )

        files = response.get("Contents", [])

        return render_template(
            "admin_documents.html",
            files=files
        )

    except Exception as e:

        return render_template(
            "admin_documents.html",
            files=[],
            error=f"Unable to load documents: {str(e)}"
        )


# ================= STUDENT DOCUMENTS =================

@app.route("/my-documents")
def my_documents():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("role") != "student":
        return redirect(url_for("admin_documents"))

    try:

        response = s3.list_objects_v2(
            Bucket=S3_BUCKET
        )

        all_files = response.get(
            "Contents",
            []
        )

        user_id = session.get("user_id")

        prefix = f"student_{user_id}_"

        files = [
            file
            for file in all_files
            if file["Key"].startswith(prefix)
        ]

        return render_template(
            "my_documents.html",
            files=files
        )

    except Exception as e:

        return render_template(
            "my_documents.html",
            files=[],
            error=f"Unable to load documents: {str(e)}"
        )


@app.route("/open-document")
def open_document():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    key = request.args.get("key")

    if not key:
        return "Document not found.", 404

    try:
        # Generate a temporary secure URL for the private S3 object
        url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": S3_BUCKET,
                "Key": key
            },
            ExpiresIn=600
        )

        return redirect(url)

    except Exception as e:
        return f"Unable to open document: {str(e)}", 500

# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ================= START APPLICATION =================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )