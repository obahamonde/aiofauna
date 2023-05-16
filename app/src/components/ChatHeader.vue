<script setup lang="ts">
const { state } = useStore()
const copy = (text: string) => {
    navigator.clipboard.writeText(text)
    state.notifications.push({
        status: 'success',
        message: 'Copied to clipboard'
    })
}

const showRef = ref(false)
const show = computed(() => showRef.value)
</script>
<template>
    <div class="header py-2" v-if="state.conversation">
        <div class="img-text">
            <div class="user-img">
                <img class="dp" :src="state.conversation.guest.picture" alt="">
            </div>
            <h4>{{ state.conversation.guest.name }}<br>
                <p class="row start items-center"
                :class="show ? '' : 'opacity-0 h-1'"
                @mouseover="showRef = true"
                @mouseleave="showRef = false"
                > <small class="text-sm  text-gray-500">{{ state.conversation.guest.ref
                }}</small>
                    <Icon @click="copy(state.conversation.guest.ref)" icon="mdi-content-copy" class="text-gray-500 mx-2" />
                </p>

                <Request :url="'/api/online/' + state.conversation.guest.ref">
                    <template v-slot="response">
                        <span v-if="response.json.online" class="online">Online</span>
                        <span v-else class="offline">Last Seen: {{ new
                            Date(Number(state.conversation.ts)).toLocaleTimeString() }}</span>
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

