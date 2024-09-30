from flask import Flask, request, jsonify, Response, stream_with_context
import requests
import sys

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate_text():
    try:
        # Extract data from the incoming request
        data = request.get_json(force=True)

        # Ensure the input contains both 'model' and 'prompt'
        if not data or 'model' not in data or 'prompt' not in data:
            return jsonify({"error": "Please provide both 'model' and 'prompt' in the request body."}), 400

        model = data['model']
        prompt = data['prompt']

        # Define the URL for Ollama API
        ollama_url = "http://localhost:11434/api/generate"

        # Prepare the request payload for Ollama
        ollama_payload = {
            "model": model,
            "prompt": prompt
        }

        # Define the headers
        headers = {'Content-Type': 'application/json'}

        # Make the internal API call to Ollama with stream=True
        response = requests.post(ollama_url, json=ollama_payload, headers=headers, stream=True)

        # Check if the response status code is 200 OK
        if response.status_code != 200:
            print(f"Ollama API returned status code {response.status_code}. Response content: {response.text}", file=sys.stderr)
            return jsonify({
                "error": f"Ollama API returned status code {response.status_code}",
                "details": response.text
            }), response.status_code

        # Stream the response to the client
        def generate():
            try:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        # Process the chunk if necessary
                        yield chunk
            except GeneratorExit:
                response.close()
                raise

        # Return a streaming response
        return Response(stream_with_context(generate()), content_type=response.headers.get('Content-Type'))

    except Exception as e:
        print(f"Exception in generate_text: {str(e)}", file=sys.stderr)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
