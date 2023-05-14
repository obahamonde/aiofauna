<script setup lang="ts">
const { state } = useStore()
</script>

<template>
    <Request :url="'/api/conversations/'+state.user.ref">
    <template v-slot="responses">
    <div class="chat-list">

        <!--chat item -->
        <div class="chat-box" v-for="response in responses.$"
        @click="state.conversation=response">
        >
            <div class="img-box">
                <img class="img-cover"
                    :src="response.users[0].picture"
                    alt="">
            </div>
            <div class="chat-details">
                <div class="text-head">
                    <h4>{{ response.users[0].name.split(" ")[0] }}</h4>
                    <span class="time unread text-xs row">{{ new Date(Number(response.ts)).toLocaleTimeString() }}</span>
                </div>
                <div class="text-message">
                    <p>{{ response.messages.length > 0 ? response.messages[-1].text : '[Start the conversation]' }}</p>
                    <b>1</b>
                </div>
            </div>
        </div>
    </div>
</template>
</Request>
</template>