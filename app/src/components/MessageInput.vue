<template>
  <div class="chatbox-input">
    <i class="fa-regular fa-face-grin"></i>
    <i
      class="fa-sharp fa-solid fa-paperclip"
      @click="showModal = !showModal"
    ></i>
    <input
      type="text"
      placeholder="Type a message"
      v-model="message"
      @keyup.enter="postMessage()"
    />
    <i class="fa-solid fa-microphone"></i>
  </div>
  <Modal v-if="showModal" @close="showModal = false">
    <MessageUpload @upload="handleUpload($event)" />
  </Modal>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRequest } from "~/composables/request";
const { request, response } = useRequest();
const { state } = useStore();
const handleUpload = async (e: any) => {
  await request("/api/messages", {
    method: "POST",
    body: JSON.stringify({
      text: e.url,
      user: state.user.ref,
      conversation: state.conversation.ref,
      kind: e.type,
    }),
  });
};
const postMessage = async () => {
  if (!state.conversation.ref || !state.user.ref || !message.value) {
    return;
  }
  await request("/api/messages", {
    method: "POST",
    body: JSON.stringify({
      text: message.value,
      user: state.user.ref,
      conversation: state.conversation.ref,
      kind: "TEXT",
    }),
  });
  message.value = "";
};
watch(
  () => response.value,
  (response) => {
    if (response) {
      state.conversation = response;
    }
  }
);
const message = ref("");
const showModal = ref(false);
</script>
