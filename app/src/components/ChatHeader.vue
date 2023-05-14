<script setup lang="ts">
const { state } = useStore()
</script>
<template>
     <div class="header" v-if="state.conversation">
        <div class="img-text">
            <div class="user-img">
                <img class="dp" :src="state.conversation.users[0].picture" alt="">
            </div>
            <h4>{{ state.conversation.users[0].name }}<br>
                <Request :url="'/api/online/'+state.conversation.users[0].ref">
                    <template v-slot="response">
                        <span v-if="response.$.online" class="online">Online</span>
                        <span v-else class="offline">Last Seen: {{ new Date(Number(state.conversation.ts)).toLocaleTimeString() }}</span>
                    </template>
                </Request>
            </h4>
        </div>
        <div class="nav-icons">
            <li><i class="fa-solid fa-magnifying-glass"></i></li>
            <li><i class="fa-solid fa-ellipsis-vertical"></i></li>
        </div>
    </div>
    <div v-else class="header">
        <div class="chat-slug">{{ new Date().toLocaleString() }}</div>
    </div>
</template>

