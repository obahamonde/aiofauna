<script setup lang="ts">
const { state } = useStore()
const copy = (text: string) => navigator.clipboard.writeText(text)
const val = ref(false)

</script>
<template>
     <div class="header" v-if="state.conversation">
        <div class="img-text">
            <div class="user-img">
                <img class="dp" :src="state.conversation.guest.picture" alt="">
            </div>
            <h4>{{ state.conversation.guest.name }}<br>
                <Request :url="'/api/online/'+state.conversation.guest.ref">
                    <template v-slot="response">
                        <small class="text-xs gap-4 row"  
                            @mouseover="val=true"
                            @mouseleave="val=false"
                            :class="val ? '' : 'opacity-0 fixed'"
                        >{{ state.conversation.guest.ref }}  <Icon icon="mdi-clipboard"
                            @click="copy(state.conversation.guest.ref)"
                            />   </small>
                        <span v-if="response.json.online" class="online">Online</span>
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

