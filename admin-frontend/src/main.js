import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/main.css'

const app = createApp(App)

app.config.errorHandler = (err, instance, info) => {
  console.error('Vue Error:', err, info)
}

app.use(createPinia())
app.use(router)
app.mount('#app')
