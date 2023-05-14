<template>
    <div class="chatbox-input">
        <i class="fa-regular fa-face-grin"></i>
        <i class="fa-sharp fa-solid fa-paperclip"></i>
        <input type="text" placeholder="Type a message" v-model="message">
        <i class="fa-solid fa-microphone"></i>
    </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'
const message = ref("")
</script>
  