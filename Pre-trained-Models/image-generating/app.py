from flask import Flask, render_template, request, send_file, flash
from huggingface_hub import InferenceClient
from huggingface_hub.utils._http import HfHubHTTPError

import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # needed for flash messages

client = InferenceClient(
    provider="together",
    api_key='hf_',#"",
)

# output is a PIL.Image object


@app.route('/', methods=['GET', 'POST'])
def index():
    image_generated = False
    error_message = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        try:
            image = client.text_to_image(
                prompt,
                model="black-forest-labs/FLUX.1-schnell",
            )
            print(image)
            image_path = os.path.join('static', 'ma.jpg')
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            image_generated = True

        except HfHubHTTPError as e:
            # You can catch specific HF errors here
            error_message = f"Error generating image: {str(e)}"
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"

    return render_template('index.html', image_generated=image_generated, error=error_message)

@app.route('/download')
def download():
    return send_file('static/ma.jpg', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
# homik55016@cigidea.com
