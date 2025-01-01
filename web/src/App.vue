<template>
  <div class="main-bg h-full w-full">
    <div class="container mx-auto">
      <div class="h-screen flex flex-col justify-center items-center">
        <div class="flex flex-col w-fit gap-2">
          <textarea class="bg-[#ffffff5c] focus:bg-[#ffffffc2] outline-none py-3 px-4 rounded-xl" v-model="paragraph" rows="8" cols="100"></textarea>
          <div class="w-fit px-3 py-1 text-white rounded-xl" :class="{'bg-zinc-600': ongoingRequest, 'bg-black': !ongoingRequest}">
            <input type="button" id="requestButton" value="Send" @click="handleRequest()"/>
            <svg v-if="ongoingRequest" aria-hidden="true" class="inline w-4 h-4 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import axios from 'axios'

  let paragraph = "";
  const ongoingRequest = ref(false);

  let cancelRequest;

  function handleRequest() {
    const button = document.getElementById('requestButton');
    button.disabled = true; // Disable the button while loading
    ongoingRequest.value = true;

    // Set a timeout to cancel the request after 3 seconds
    const timeout = setTimeout(() => {
      if (cancelRequest) {
        cancelRequest('Request timed out');
        alert('Request timed out');

        // Re-enable button
        ongoingRequest.value = false;
        button.disabled = false;
      }
    }, 10000);

    // Create an Axios CancelToken to be able to cancel the request
    const source = axios.CancelToken.source();
    cancelRequest = source.cancel;

    axios.post('http://127.0.0.1:8000/predict_sentiment/', {
        paragraph: paragraph
    }, {
        cancelToken: source.token
    })
    .then(response => {
        console.log(response);
        // printResponse(response);
    })
    .catch(error => {
        if (axios.isCancel(error)) {
            console.log('Request cancelled:', error.message);
        } else {
            console.error('Error occurred:', error);
        }
    })
    .finally(() => {
      // Re-enable button
      ongoingRequest.value = false;
      button.disabled = false;
      clearTimeout(timeout); // Clear the timeout
    });
  }
    // Process sentiment data and map it into an array of objects
    // processSentiment(wordSentiments) {
    //   this.wordSentiments = wordSentiments.map(([word, sentiment, probabilities]) => {
    //     return {
    //       word: word,
    //       sentiment: sentiment,
    //       color: this.getColorBasedOnSentiment(sentiment, probabilities)
    //     };
    //   });
    // },

    // // Determine the color based on the sentiment
    // getColorBasedOnSentiment(sentiment, probabilities) {
    //   // Apply color based on sentiment type (as given by the FastAPI response)
    //   if (sentiment === 'pos') return 'green'; // Positive sentiment
    //   else if (sentiment === 'neg') return 'red'; // Negative sentiment
    //   else return 'gray'; // Neutral sentiment (default to gray)
    // }
  // }
</script>

<style scoped>

</style>
