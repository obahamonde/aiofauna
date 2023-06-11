<script setup lang="ts">
const { state } = useStore();
const selectedConversation = ref(null);

const setConversation = async (conversation: any) => {
  selectedConversation.value = conversation;
};

const extractContact = (response: any) => {
  const owner = response.owner;
  const guest = response.guest;

  return owner.ref == state.user.ref ? guest : owner;
};

watch(selectedConversation, (newConversation) => {
  state.conversation = newConversation;
});
</script>

<template>
  <div v-if="state.user && state.user.ref">
    <Request :url="'/api/conversations/' + state.user.ref">
      <template #="responses">
        <div class="chat-list">
          <!--chat item -->
          <div
            v-for="response in responses.json"
            @click="setConversation(response)"
          >
            <div
              class="chat-box"
              v-if="extractContact(response).ref !== state.user.ref"
            >
              <div class="img-box">
                <img
                  class="img-cover"
                  :src="extractContact(response).picture"
                  :alt="extractContact(response).ref"
                />
              </div>
              <div class="chat-details">
                <div class="text-head">
                  <h4>{{ extractContact(response).name.split(" ")[0] }}</h4>
                  <span class="time unread text-xs row">{{
                    new Date(Number(response.ts)).toLocaleTimeString()
                  }}</span>
                </div>
                <div class="text-message">
                  <p>
                    {{
                      response.messages.length > 0
                        ? response.messages[response.messages.length - 1].text
                        : "[Start the conversation]"
                    }}
                  </p>
                  <b>{{ response.messages.length }}</b>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Request>
  </div>
</template>
