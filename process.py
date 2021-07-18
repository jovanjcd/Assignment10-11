from flask import Flask, render_template, request, Response, redirect, url_for
import cv2, imutils
app = Flask(__name__)

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture('videos/video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

class VideoCamera2(VideoCamera):
    def __init__(self):
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        self.video = cv2.VideoCapture(0)

# Route for handling the login page logic
@app.route('/', methods=['POST', 'GET'])
def log_in():
    error = None
    if request.method == 'POST':
        if request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('gate_way'))
    return render_template('log_in.html', error=error)

@app.route('/gate_way', methods=['POST', 'GET'])
def gate_way():
    if "static_feed" in request.form:
        return render_template('static_feed.html')
    elif "live_feed" in request.form:
        return render_template('live_feed.html')
    return render_template('gate_way.html')

def gen(camera):
    ret, img = camera.read()
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/static_feed')
def static_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live_feed')
def live_feed():
    return Response(gen(VideoCamera2()),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, host='10.0.0.177',port=9999,threaded=True)
