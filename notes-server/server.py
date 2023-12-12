from flask import Flask,request,jsonify 
import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS

CREATE_NOTES_TABLE = (
    "CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY, title VARCHAR(100), content VARCHAR(500));"
)

INSERT_NOTE = "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id;"
UPDATE_NOTE = "UPDATE notes SET (title, content) = (%s, %s) WHERE id = %s"
DELETE_NOTE = "DELETE FROM notes WHERE id = %s"

load_dotenv()

app = Flask(__name__)
CORS(app)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.get("/notes")
def get_notes():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM notes;')
            notes = cursor.fetchall()
            response = [{'id': note[0], 'title':note[1], 'content':note[2]} for note in notes]
    # response = jsonify(notes)
    return response



@app.post("/api/notes")
def create_note():
    data = request.get_json()
    print(data)
    title = data['title']
    content = data['content']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_NOTES_TABLE)
            cursor.execute(INSERT_NOTE, (title,content,))
            note_id = cursor.fetchone()[0]
            notes = {'id': note_id, 'title':title, 'content':content}
    response = notes
    return response

@app.put("/api/notes/<int:note_id>")
def update_note(note_id):
    data = request.get_json()
    title = data['title']
    content = data['content']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_NOTE, (title,content,note_id,))
    return {"id":note_id, "message": f"Note {title} updated."}, 200

@app.delete("/api/notes/<int:note_id>")
def delete_note(note_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_NOTE, (note_id,))
    return {"id":note_id, "message": f"Note deleted"}, 204

if __name__=='__main__':
    app.run(debug=True)