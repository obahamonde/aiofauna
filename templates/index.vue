<template>
    <div class="index">{{ data }}</div>
</template>

<script setup lang="ts">
const data = ref('Hello World')
</script>

<style scoped>
.index {
    color: red;
}
</style>