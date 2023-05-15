<script setup lang="ts">
const { state } = useStore()
const selectedConversation = ref(null)

const setConversation = async(conversation: any) => {
    selectedConversation.value = conversation
   
}

watch(selectedConversation, (newConversation) => {
    state.conversation = newConversation
})
</script>

<template>
    <Request :url="'/api/conversations/'+state.user.ref">
    <template v-slot="responses">
    <div class="chat-list">

        <!--chat item -->
        <div class="chat-box" v-for="response in responses.json"
        @click="setConversation(response)">
        
            <div class="img-box">
                <img class="img-cover"
                    :src="response.guest.picture"
                    :alt="response.guest.ref">
            </div>
            <div class="chat-details">
                <div class="text-head"> 
                    <h4>{{ response.guest.name.split(' ')[0] }}</h4>
                    <span class="time unread text-xs row">{{ new Date(Number(response.ts)).toLocaleTimeString() }}</span>
                </div>
                <div class="text-message">
                    <p>{{ response.messages.length > 0 ? response.messages.reverse()[0].text : '[Start the conversation]' }}</p>
                    <b>{{ response.messages.reduce((acc:any, cur:any) => cur.read ? acc : acc + 1, 0) }}</b>
                </div>
            </div>
        </div>
    </div>
</template>
</Request>
</template>