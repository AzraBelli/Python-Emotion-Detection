"""
Modules:
    Flask: Web framework for building the web application.
    emotion_detector: Custom function to interact with the emotion detection API.
"""
from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)  # Correct Flask app naming convention

@app.route("/emotionDetector")
def analyze_emotion():
    """
    API endpoint to analyze the emotions in a given text.

    Retrieves the 'textToAnalyze' parameter from the request and processes it 
    using the emotion_detector function. If the parameter is missing or invalid, 
    it returns a 400 Bad Request error.

    Returns:
        JSON response containing emotion scores for anger, disgust, fear, joy, 
        and sadness, along with the dominant emotion.
    """
    text_to_analyze = request.args.get('textToAnalyze')

    if not text_to_analyze:  # Check for missing parameter
        return jsonify({"error": "Missing 'textToAnalyze' parameter"}), 400

    response = emotion_detector(text_to_analyze)

    if response['dominant_emotion'] is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400
    emotion_output = (
    f"For the given statement, the system response is "
    f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
    f"'fear': {response['fear']}, 'joy': {response['joy']}, "
    f"and 'sadness': {response['sadness']}. The dominant emotion is "
    f"{response['dominant_emotion']}."
)

    return jsonify({"message": emotion_output})

@app.route("/")
def render_index_page():
    """
    Renders the index.html page.

    This function serves the homepage of the web application, 
    providing a user interface for text input.
    
    Returns:
        Rendered HTML page.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Debug mode enabled
