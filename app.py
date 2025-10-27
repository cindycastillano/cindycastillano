from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# ---------- Home Route ----------
@app.route('/')
def home():
    return "Welcome to my Flask API! Visit /dashboard to see the dashboard."

# ---------- Student Data Route ----------
@app.route('/student', methods=['GET'])
def get_student():
    name = request.args.get('name', 'Your Name')
    grade = request.args.get('grade', 10)
    section = request.args.get('section', 'Zechariah')

    return jsonify({
        "name": name,
        "grade": grade,
        "section": section
    })

# ---------- Dashboard Route ----------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Default student data
    student = {
        "name": "Your Name",
        "grade": 10,
        "section": "Zechariah"
    }

    # If form submitted, update the student info
    if request.method == 'POST':
        student["name"] = request.form.get("name", student["name"])
        student["grade"] = request.form.get("grade", student["grade"])
        student["section"] = request.form.get("section", student["section"])

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Dashboard</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #f5f7fa; margin: 0; padding: 40px; }
            .container { max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 12px;
                         box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
            h1 { text-align: center; color: #333; }
            form { margin-top: 20px; }
            label { display: block; margin-top: 10px; font-weight: bold; color: #444; }
            input { width: 100%; padding: 10px; margin-top: 5px; border-radius: 6px; border: 1px solid #ccc; }
            button { margin-top: 20px; padding: 10px 20px; background: #007bff; border: none; color: white; border-radius: 6px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .info { margin-top: 25px; background: #f9fafb; padding: 15px; border-radius: 8px; }
            .footer { text-align: center; margin-top: 20px; color: #888; }
            .json-link { display: inline-block; margin-top: 10px; color: #007bff; text-decoration: none; }
            .json-link:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Student Dashboard</h1>

            <form method="POST">
                <label>Name:</label>
                <input type="text" name="name" value="{{ student.name }}">
                
                <label>Grade:</label>
                <input type="number" name="grade" value="{{ student.grade }}">
                
                <label>Section:</label>
                <input type="text" name="section" value="{{ student.section }}">
                
                <button type="submit">Update Info</button>
            </form>

            <div class="info">
                <h3>Current Student Info</h3>
                <p><b>Name:</b> {{ student.name }}</p>
                <p><b>Grade:</b> {{ student.grade }}</p>
                <p><b>Section:</b> {{ student.section }}</p>
                <a href="/student?name={{ student.name }}&grade={{ student.grade }}&section={{ student.section }}" class="json-link" target="_blank">
                    View as JSON →
                </a>
            </div>

            <div class="footer">
                <p>Made with ❤️ using Flask</p>
            </div>
        </div>
    </body>
    </html>
    """

    return render_template_string(html, student=student)

# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)
