<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue"
const { state } = useStore()
const { logout } = useAuth0()
</script>
<template>
  <div class="header">
    <div class="user-img">
      <img class="dp" :src="state.user.picture" :alt="state.user.name" @click="logout()">
    </div>
    <div class="nav-icons">
      <li><i class="fa-solid fa-users"></i></li>
      <li><i class="fa-solid fa-message">
        </i></li>
      <li><i class="fa-solid fa-ellipsis-vertical"></i></li>
    </div>
  </div>
</template>