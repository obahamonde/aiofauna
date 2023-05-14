<script setup lang="ts">
import Notifier from "./components/Notifier.vue";
import { useAuth0 } from '@auth0/auth0-vue'
import { watch, ref } from 'vue'
const { state } = useStore()
const { isAuthenticated, loginWithRedirect, getAccessTokenSilently, user } = useAuth0()

watch(user, async () => {
  user.value ? state.user = await authorize() : state.user = null
})

const authorize = async () => {
  const token = await getAccessTokenSilently()
  const res = await fetch('http://localhost:3000/api/auth?token=' + token)
  const data = await res.json()
  state.notifications.push({ message: "Welcome " + user.value.name, status: "success" })
  return data
}

</script>
<template>
  <Notifier />
  <div v-if="state.user && isAuthenticated">
    <div class="background-green"></div>
    <div class="main-container">
      <RouterView />
    </div>
  </div>
  <div v-else>
    <h1>Not Authenticated</h1>
    <button class="btn btn-login" @click.prevent="loginWithRedirect()">Login</button>
  </div>
  <Credits />
</template>