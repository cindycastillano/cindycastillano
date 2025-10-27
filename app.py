from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# ---------- In-memory database ----------
students = [
    {"id": 1, "name": "John Doe", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Jane Smith", "grade": 11, "section": "A"}
]

# ---------- Home Redirect ----------
@app.route('/')
def home():
    return redirect(url_for('dashboard'))

# ---------- API: Get All Students ----------
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# ---------- API: Get One Student ----------
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    for s in students:
        if s["id"] == student_id:
            return jsonify(s)
    return jsonify({"error": "Student not found"}), 404

# ---------- Dashboard ----------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global students

    # Handle new student addition
    if request.method == 'POST':
        name = request.form.get("name")
        grade = request.form.get("grade")
        section = request.form.get("section")
        if name and grade and section:
            new_student = {
                "id": len(students) + 1,
                "name": name,
                "grade": int(grade),
                "section": section
            }
            students.append(new_student)
        return redirect(url_for('dashboard'))

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Dashboard</title>
        <style>
            body { font-family: 'Poppins', sans-serif; background: #f0f4f8; margin: 0; padding: 40px; }
            .container { max-width: 900px; margin: auto; background: white; padding: 30px; border-radius: 15px;
                         box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
            h1 { text-align: center; color: #333; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; border-bottom: 1px solid #ddd; text-align: center; }
            th { background-color: #007bff; color: white; }
            tr:hover { background-color: #f1f1f1; }
            .form-container { background: #f9fafb; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
            label { display: block; margin-top: 10px; font-weight: 600; color: #444; }
            input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; margin-top: 5px; }
            button { padding: 8px 15px; border: none; border-radius: 6px; cursor: pointer; }
            .add-btn { background: #28a745; color: white; margin-top: 10px; }
            .add-btn:hover { background: #218838; }
            .edit-btn { background: #ffc107; color: white; }
            .edit-btn:hover { background: #e0a800; }
            .delete-btn { background: #dc3545; color: white; }
            .delete-btn:hover { background: #c82333; }
            .footer { text-align: center; color: #888; margin-top: 25px; }
            a { text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Student Management Dashboard</h1>

            <div class="form-container">
                <h3>Add New Student</h3>
                <form method="POST">
                    <label>Name:</label>
                    <input type="text" name="name" required>
                    
                    <label>Grade:</label>
                    <input type="number" name="grade" required>
                    
                    <label>Section:</label>
                    <input type="text" name="section" required>
                    
                    <button type="submit" class="add-btn">+ Add Student</button>
                </form>
            </div>

            <h3>Current Students</h3>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Grade</th>
                    <th>Section</th>
                    <th>Actions</th>
                </tr>
                {% for s in students %}
                <tr>
                    <td>{{ s.id }}</td>
                    <td>{{ s.name }}</td>
                    <td>{{ s.grade }}</td>
                    <td>{{ s.section }}</td>
                    <td>
                        <a href="/edit/{{ s.id }}"><button class="edit-btn">Edit</button></a>
                        <a href="/delete/{{ s.id }}"><button class="delete-btn">Delete</button></a>
                    </td>
                </tr>
                {% endfor %}
            </table>

            <div class="footer">
                <p>Made with ❤️ using Flask</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, students=students)

# ---------- Edit Student ----------
@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    global students
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        student["name"] = request.form.get("name", student["name"])
        student["grade"] = int(request.form.get("grade", student["grade"]))
        student["section"] = request.form.get("section", student["section"])
        return redirect(url_for('dashboard'))

    html = """
    <html>
    <head>
        <title>Edit Student</title>
        <style>
            body { font-family: Arial; background-color: #f4f6f8; padding: 40px; }
            .container { max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px;
                         box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            h2 { text-align: center; color: #333; }
            label { display: block; margin-top: 10px; font-weight: bold; }
            input { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #ccc; }
            button { margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; }
            button:hover { background: #0056b3; }
            a { text-decoration: none; display: inline-block; margin-top: 10px; color: #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Edit Student</h2>
            <form method="POST">
                <label>Name:</label>
                <input type="text" name="name" value="{{ student.name }}" required>
                
                <label>Grade:</label>
                <input type="number" name="grade" value="{{ student.grade }}" required>
                
                <label>Section:</label>
                <input type="text" name="section" value="{{ student.section }}" required>
                
                <button type="submit">Update</button>
            </form>
            <a href="/dashboard">← Back to Dashboard</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, student=student)

# ---------- Delete Student ----------
@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return redirect(url_for('dashboard'))

# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)
