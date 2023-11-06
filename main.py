from flask import Flask, render_template, request, send_file
from face_detection import process_video
from compare_faces import compare_faces

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video_route():
    video = request.files['video']
    video.save('uploaded_video.mp4')  # Save uploaded video
    process_video('uploaded_video.mp4', 'static/faces')
    return 'Video processed successfully!'

@app.route('/download_faces')
def download_faces():
    # Add code to zip and download faces here
    return send_file('path_to_zip_file.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
