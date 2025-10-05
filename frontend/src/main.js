// src/main.js
import 'vuetify/styles'; // Add this line if not already present
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './vuetify';

const app = createApp(App);

app.use(store);
app.use(router);
app.use(vuetify);

app.mount('#app');
