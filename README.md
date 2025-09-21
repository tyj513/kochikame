 

# 烏龍派出所 LINE Bot

This is a LINE Bot created with Python and Flask that allows users to search for images and videos from the anime series "烏龍派出所". Users can interact with the bot to get random images/videos or search with specific keywords.

## Features

  * **Image Search:** Search for images from the show by providing keywords.
  * **Video Search:** Search for specific video clips.
  * **Random Image/Video:** Get a random image or video from the collection.
  * **Interactive Menu:** A simple menu with quick reply buttons for easy navigation.

## How to Use the Bot

Once the bot is running and you've added it as a friend on LINE, you can use the following commands:

  * **`menu`**: Displays the main menu with options to get a random image or video.
  * **`抽` or `抽圖`**: Sends a random image.
  * **`抽影片`**: Sends a random video.
  * **`v` + [keyword]** (e.g., `v阿兩`): Searches for videos related to the keyword.
  * **[keyword]** (e.g., `本田`): Searches for images related to the keyword.

## Project Structure

```
.
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku deployment configuration
├── .gitignore                  # Files and directories to ignore in git
├── merged_output_with_url.json # Image data
├── merge_video_output_with_url.json # Video data
└── .env                        # Environment variables (not included)
```

## Setup and Installation

### Prerequisites

  * Python 3.12
  * A LINE Developers account and a Messaging API channel.
  * `ngrok` or a similar tool for local development to expose your local server to the internet.
  * A platform to deploy the bot (e.g., Heroku).

### Local Development

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your LINE Channel Access Token and Channel Secret:

    ```
    LINE_CHANNEL_ACCESS_TOKEN=<Your_Channel_Access_Token>
    LINE_CHANNEL_SECRET=<Your_Channel_Secret>
    ```

4.  **Run the Flask application:**

    ```bash
    flask run
    ```

5.  **Expose your local server:**
    Use `ngrok` to create a public URL for your local server:

    ```bash
    ngrok http 5000
    ```

6.  **Set the Webhook URL:**
    In your LINE Developers Console, go to your channel's "Messaging API" settings and set the Webhook URL to the `https` URL provided by `ngrok`, followed by `/callback`. For example: `https://your-ngrok-url.ngrok.io/callback`.

### Deployment (Heroku)

This project is set up for deployment on Heroku.

1.  **Create a Heroku app.**
2.  **Connect your Heroku app to your Git repository.**
3.  **Set the environment variables in your Heroku app's settings:**
      * `LINE_CHANNEL_ACCESS_TOKEN`
      * `LINE_CHANNEL_SECRET`
4.  **Deploy the application.** Heroku will use the `Procfile` to start the `gunicorn` web server.
5.  **Update the Webhook URL** in your LINE Developers Console to your Heroku app's URL, followed by `/callback`.

## Dependencies

  * [Flask](https://flask.palletsprojects.com/): A lightweight web framework for Python.
  * [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python): A Python SDK for the LINE Messaging API.
  * [gunicorn](https://gunicorn.org/): A Python WSGI HTTP Server for UNIX.
  * [python-dotenv](https://github.com/theskumar/python-dotenv): Reads key-value pairs from a `.env` file and can set them as environment variables.

## Data Files

  * `merged_output_with_url.json`: Contains a JSON array of objects, where each object represents an image and includes the episode number, image name, recognized text, and a URL to the image.
  * `merge_video_output_with_url.json`: Contains a JSON array of objects for video clips with similar metadata.

-----
