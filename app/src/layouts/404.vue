<script setup lang="ts">
const router = useRouter();
</script>
<template>
  <main p="x4 y10" text="center teal-700 dark:gray-200">
    404 Not Found
    <button class="btn-get" @click="router.back()">Go Back</button>
  </main>
</template>
