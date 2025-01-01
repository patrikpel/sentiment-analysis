# A sentiment analysis project by Patrik
This project demonstrates my skills in developing a full stack application with Python (FastAPI and FastAI), and a frontend web app that runs on Vue + TailwindCSS with Axios providing API call functionalities.

My developmental blade with Python is (at this moment) somewhat dull so I wrote the API using FastAI's and FastAPI's documentations as a reference with some help from Claude. I can still probably answer most of the question a user might have regarding it's logic.

## Setup 
### Step 1: Set how many rows you want the AI to download from the file (optional)
The app has a default value of 2000, but if you want more or less accuracy, you can modify this in the [SentimentalAnalysis.py file in the function called `load_data`, on the row where data is loaded](https://github.com/patrikpel/sentiment-analysis/blob/d9b02d983faae0ed4ce47fb32a64eaa14e377924/api/SentimentAnalysis.py#L27).


### Step 1: Run the Docker images
The first step in running this project is building and running the Docker images for the API and web app. Run this command: \
`docker-compose -f "docker-compose-dev.yaml" up --build`