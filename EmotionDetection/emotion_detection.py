import requests
import json

def emotion_detector(text_to_analyse):
    """
    Function to detect emotions from a given text using an external API.

    Args:
        text_to_analyse (str): The input text that needs to be analyzed for emotions.

    Returns:
        dict: A dictionary containing emotion predictions and the dominant emotion.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = {"raw_document": {"text": text_to_analyse}}
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Send POST request
    response = requests.post(url, json=myobj, headers=header)

    # Initialize emotion variables
    anger, disgust, fear, joy, sadness, emotion, dominant_emotion = None, None, None, None, None, None, None

    # Handle response based on status code
    if response.status_code == 400:
        return {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness,
            'dominant_emotion': dominant_emotion
        }

    elif response.status_code == 200:
        try:
            formatted_response = json.loads(response.text)
            emotion_data = formatted_response['emotionPredictions'][0]['emotion']

            anger = emotion_data.get('anger', None)
            disgust = emotion_data.get('disgust', None)
            fear = emotion_data.get('fear', None)
            joy = emotion_data.get('joy', None)
            sadness = emotion_data.get('sadness', None)

            emotion = emotion_data
            dominant_emotion = max(emotion, key=emotion.get)

        except (KeyError, IndexError, json.JSONDecodeError) as e:
            # If there is an error in parsing the response, we handle it and keep None as values
            print(f"Error parsing response: {e}")

    return {
        'anger': anger,
        'disgust': disgust,
        'fear': fear,
        'joy': joy,
        'sadness': sadness,
        'dominant_emotion': dominant_emotion
    }
