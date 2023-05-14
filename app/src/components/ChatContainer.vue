<script setup lang="ts">
const { state } = useStore()
</script>
<template>
        <div class="chat-container">
<div v-if="state.conversation">    <Sse :ref-param="state.conversation.ref" >
        <template v-slot="message">
        <div>
        <div :class="state.user.ref === message.$.user ? 'message-box my-message':'message-box friend-message'">
            <p>{{ message.$.text }}<br><span>{{ new Date(Number(message.$.ts)).toLocaleString() }}</span></p>
        </div>
    </div>
</template>
</Sse>
</div>

<div v-else class="chat-container">
        <h1 class="text-center px-4 py-2 rounded-lg bg-gray-300 w-64 mx-auto">Select a conversation to start chatting</h1>
    </div>
</div>

</template>