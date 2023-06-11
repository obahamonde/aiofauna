<script setup lang="ts">
const { state } = useStore();
const copy = (text: string) => navigator.clipboard.writeText(text);
const val = ref(false);
const contact = computed(() => {
  if (!state.conversation) return;
  const ctc =
    state.conversation.guest.name == state.user.name
      ? state.conversation.owner
      : state.conversation.guest;
  return ctc;
});
</script>
<template>
  <div class="header py-2" v-if="state.conversation && contact">
    <div class="img-text">
      <div class="user-img">
        <img class="dp" :src="contact.picture" alt="" />
      </div>
      <h4>
        {{ contact.name }}
        <Request :url="'/api/online/' + contact.ref">
          <template v-slot="response">
            <small
              class="text-xs gap-4 row"
              @mouseover="val = true"
              @mouseleave="val = false"
              :class="val ? '' : 'opacity-0 fixed'"
              >{{ contact.ref }}
              <Icon icon="mdi-clipboard" @click="copy(contact.ref)" />
            </small>
            <span v-if="response.json.online" class="online">Online</span>
            <span v-else class="offline"
              >Last Seen:
              {{
                new Date(Number(state.conversation.ts)).toLocaleTimeString()
              }}</span
            >
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
