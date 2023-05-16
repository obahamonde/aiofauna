<script setup lang="ts">
const showModal = ref(false);
</script>
<template>
  <div class="search-container">
    <div class="input">
      <i
        class="fa-solid fa-magnifying-glass"
        @click="showModal = !showModal"
      ></i>
      <input type="text" placeholder="Search or start new chat" />
    </div>
    <i class="fa-sharp fa-solid fa-bars-filter"></i>
    <Modal v-if="showModal" @close="showModal = false"> </Modal>
  </div>
</template>
