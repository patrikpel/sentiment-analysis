import './assets/style.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import PrimeVue from 'primevue/config';

const app = createApp(App)
app.use(VueAxios, axios)
app.use(PrimeVue);

app.use(router)

app.mount('#app')
