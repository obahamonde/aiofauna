import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from "pinia";
import { createAuth0 } from "@auth0/auth0-vue";
import { Icon } from "@iconify/vue";

import routes from "virtual:generated-pages";
import App from "./App.vue";

import "@unocss/reset/tailwind.css";
import "./styles/main.css";
import "uno.css";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

createApp(App)
  .use(createPinia())
  .use(
    createAuth0({
      domain: "dev-tvhqmk7a.us.auth0.com",
      clientId: "53p0EBRRWxSYA3mSywbxhEeIlIexYWbs",
      authorizationParams: {
        redirect_uri: window.location.origin,
      },
    })
  )
  .use(router)
  .component("Icon", Icon)
  .mount("#app");
