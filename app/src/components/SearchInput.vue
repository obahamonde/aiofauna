  
<script setup lang="ts">
const message = ref("")
</script>

<template>
    <div class="chatbox-input px-4">
        <Icon icon="mdi-emoticon-outline" icon-btn />
        <Icon icon="mdi-paperclip" icon-btn />
        <input type="text" placeholder="Type a message" v-model="message">
        <Icon icon="mdi-microphone" icon-btn></Icon>
    </div>
</template>
