<script setup lang="ts">
import { useSSE } from "~/composables/sse";

const props = defineProps({
  url: {
    type: String,
    required: false,
    default: "/api/sse",
  },
  query: {
    type: String,
    required: true,
  },
});

const { messages, eventSource, status: thisStatus } = useSSE(props);
const status = computed<"OPEN" | "CLOSED" | "CONNECTING">(
  () => thisStatus.value
);
watch(eventSource, (newVal, oldVal) => {
  if (oldVal) {
    oldVal.close();
  }
  eventSource.value = newVal;
});
</script>
<template>
  <div v-if="status === 'OPEN'">
    <div v-for="message in messages">
      <slot :sse="message"></slot>
    </div>
  </div>
  <div v-else-if="status === 'CONNECTING'">
    <slot name="loading">
      <Icon icon="mdi-loading" animate-spin x2 />
    </slot>
  </div>
  <div v-else-if="status === 'CLOSED'">
    <slot name="error">
      <p class="text-error">Connection closed</p>
    </slot>
  </div>
</template>
