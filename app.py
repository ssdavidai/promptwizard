from flask import Flask, request, render_template
import openai
import requests

# Set your OpenAI API key
openai.api_key = "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"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the audio file from the request object
        audio_file = request.files['audio_file'].read()

        # Upload the audio file to the server and get its URL
        files = {'file': ('audio.mp3', audio_file)}
        response = requests.post('https://api.myserver.com/upload', files=files)
        audio_url = response.json()['url']

        # Get the prompt text from the request object
        prompt = request.form['prompt']

        # Translate the audio file to text
        transcript = openai.Audio.translate("whisper-1", io.BytesIO(audio_file))

        # Use the transcript and prompt text as input for GPT-3.5-turbo
        prompt_final = f"{prompt} {transcript}"
        model_engine = "gpt-4"

        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[
            {"role": "system", "content": "You are a scrum master who takes notes using markdown format using the Mermaid syntax."},
            {"role": "user", "content": f"{prompt_final}"}
          ]
        )

        reply = response['choices'][0]['message']['content']

        # Pass the reply text to the template
        return render_template('home.html', reply=reply)

    # Render the upload form
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
