<script setup lang="ts">
const { state } = useStore()
</script>
<template>
  
  
        <div class="chat-container">
        <div v-if="state.conversation">
            <Request :url="'/api/messages/'+state.conversation.ref" >
    <template v-slot="response">
            <div v-for="message in response.json">
                        <div
                            :class="state.user.ref === message.owner ? 'message-box my-message' : 'message-box friend-message'">
                            <p>{{ message.text }}<br><span>{{ new Date(Number(message.ts)).toLocaleString() }}</span>
                            </p>
                        </div>
                    </div>     </template>
    </Request>
  
            <Sse :query="state.conversation.ref">
                <template v-slot="message">
                    <div>
                        <div
                            :class="state.user.ref === message.sse.user ? 'message-box my-message' : 'message-box friend-message'">
                            <p>{{ message.sse.text }}<br><span>{{ new Date(Number(message.sse.ts)).toLocaleString() }}</span>
                            </p>
                        </div>
                    </div>
                </template>
            </Sse>
   
        </div>

        <div v-else class="chat-container">
            <h1 class="text-center px-4 py-2 rounded-lg bg-gray-300 w-64 mx-auto">Select a conversation to start chatting
            </h1>
        </div>        </div>
      
</template>