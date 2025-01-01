<template>
  <div class="main-bg h-full w-full">
    <div class="container mx-auto">
      <div class="h-screen flex flex-col justify-center items-center">
        <div class="flex flex-col w-fit gap-2 w-full">
          <textarea class="bg-[#ffffff5c] focus:bg-[#ffffffc2] outline-none py-3 px-4 rounded-xl mx-4 lg:mx-0" v-model="paragraph" rows="8" cols="100"></textarea>
          <div class="w-fit px-3 py-1 text-white rounded-xl mx-4 lg:mx-0" :class="{'bg-zinc-600': ongoingRequest, 'bg-black': !ongoingRequest}">
            <input type="button" id="requestButton" value="Send" @click="getSentiment()"/>
            <svg v-if="ongoingRequest" aria-hidden="true" class="inline w-4 h-4 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
            </svg>
          </div>
          <div class="bg-[#2f2f2f69] px-3 py-1 rounded-xl">
            <div v-if="responseComputed && responseComputed.length > 0" class="flex flex-row flex-wrap gap-1">
              <span v-for="(item, index) in responseComputed" :key="index" :style="'color:'+item.textcolor">
                {{ item.word }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed } from "vue";
  import axios from 'axios'

  let paragraph = "";
  const ongoingRequest = ref(false);
  let cancelRequest;

  async function handleRequest() {
    const button = document.getElementById('requestButton');
    button.disabled = true; // Disable the button while loading
    ongoingRequest.value = true;

    // Set a timeout to cancel th§e request after 10 seconds
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

    let apiResponse = null;

    try {
        // Perform the Axios request
        const response = await axios.post('http://127.0.0.1:8000/predict_sentiment/', {
            paragraph: paragraph
        }, {
            cancelToken: source.token
        });

        // Return response
        return response?.data?.word_sentiments ?? false;
    } catch (error) {
        if (axios.isCancel(error)) {
            console.log('Request cancelled:', error.message);
        } else {
            console.error('Error occurred:', error);
        }
    } finally {
        // Re-enable the button after the request is done
        ongoingRequest.value = false;
        button.disabled = false;
        clearTimeout(timeout); // Clear the timeout
    }
  }

  let processedSentiments = ref([]);
  const responseComputed = computed(() => {
    return processedSentiments.value;
  });

  async function getSentiment() {
    const responseFromAPI = await handleRequest();
    console.log(responseFromAPI);
    if (responseFromAPI) {
      processedSentiments.value = processSentiment(responseFromAPI);
    }
  }

  // Process sentiment data and map it into an array of objects
  function processSentiment(wordSentiments) {
    return wordSentiments.map(([word, sentiment, probabilities]) => {
      let probablitiesObject = {
          positive: probabilities[2],
          negative: probabilities[0],
          neutral: probabilities[1]
      }; 
      console.log(probabilities)
      return {
        word: word,
        sentiment: sentiment,
        textcolor: getTextColorClassBasedOnSentiment(sentiment, probablitiesObject)
      };
    });
  }

  // Determine the color based on sentiment and probabilities, with a dynamic gradient for neutral sentiment
  function getTextColorClassBasedOnSentiment(sentiment, probabilities) {
    const posProbability = probabilities.positive || 0; // Fallback to 0 if undefined
    const negProbability = probabilities.negative || 0; // Fallback to 0 if undefined
  
    // If sentiment is positive, return green
    if (sentiment === 'positive') {
      // Use a range between light green for weak positives and a more vibrant green for strong positives
      return posProbability > 0.7 ? 'forestgreen' : 'mediumseagreen'; // Strongly positive vs weakly positive
    }
    
    // If sentiment is negative, return red
    else if (sentiment === 'negative') {
      // Use a range between dark red for strong negatives and light red for weak negatives
      return negProbability > 0.7 ? 'darkred' : 'lightcoral'; // Strongly negative vs weakly negative
    }

    // If sentiment is neutral, calculate a gradient between red and green
    else {
      // Calculate the difference between positive and negative probabilities
      const diff = Math.abs(posProbability - negProbability);

      // Apply a gradient if the difference is greater than 0.1
      if (diff >= 0.05) {
        // Calculate a smooth gradient from red to green based on the probabilities
        const ratio = posProbability / (posProbability + negProbability); // Range between 0 and 1
        const red = Math.round((1 - ratio) * 255); // Higher red for more negative
        const green = Math.round(ratio * 255); // Higher green for more positive

        // Return the RGB gradient color
        return `rgb(${red}, ${green}, 0)`; // Yellow-green for positive dominance, yellow-red for negative
      } else {
        return 'lightgray'; // Neutral sentiment when the difference is less than 0.1
      }
    }
  }
</script>

<style scoped>

</style>
