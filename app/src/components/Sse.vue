<script setup lang="ts">
import { useSSE } from "~/composables/sse"

const props = defineProps({
    url: {
      type: String,
      required: false,
        default: "/api/sse"
    },
    refParam: {
      type: String,
      required: true
    }
  });

const { messages, eventSource, status } = useSSE(props)
const conn = computed<"OPEN" | "CLOSED" | "CONNECTING">(() => status.value)
watch(eventSource, (newVal, oldVal) => {
    if (oldVal) {
        oldVal.close()
    }
    eventSource.value = newVal
})
</script>
<template>
<div v-if="conn === 'OPEN'">
    <div v-for="message in messages">
        <slot :$="message"></slot>
    </div>
</div>
<div v-else-if="conn === 'CONNECTING'">
    <slot name="loading">
        <Icon icon="mdi-loading" animate-spin x2 />
    </slot>
</div>
<div v-else-if="conn === 'CLOSED'">
    <slot name="error">
        <p class="text-error">Connection closed</p>
    </slot>
</div>
</template>