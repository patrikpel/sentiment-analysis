# A sentiment analysis project by Patrik
This project demonstrates my skills in developing a full stack application with TBD languages. Will edit this afterwards. Or not, dunno.

## Setup 
### Step 1: Build the docker image
After cloning the repository, go to the root of the repository and run \
`docker build -t sentiment-analysis .` \
to create the docker image. You can subsitute a name of your own if you want, but remember to replace it in later steps.

### Step 2: Run the docker image
After building the image, the next step is to run it in a container \
`docker run -p 8888:8888 -v ${PWD}:/home/ sentiment-analysis`
As `${PWD}` is a Windows terminal exclusive, replace it with `~/` on Linux or other equivalent that refers to current working directory of the terminal, depending on your OS.