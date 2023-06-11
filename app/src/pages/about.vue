<script setup lang="ts">
const markdown = ref("");

const fetchAboutPage = async () => {
  const { data } = await useFetch("/api/about").text();
  markdown.value = unref(data) as string;
};

onMounted(fetchAboutPage);
</script>

<template>
  <div v-html="markdown"></div>
</template>
