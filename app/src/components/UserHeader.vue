<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { state } = useStore();
const { logout } = useAuth0();
const showModal = ref(false);
const numberRef = ref("");
const { request, response } = useRequest();
const dofetch = async () => {
  const userRef = state.user.ref;
  if (!userRef) {
    return;
  }
  if (!numberRef.value || !userRef) {
    return;
  }
  await request(
    "/api/new_conversation/" + userRef + "?contact=" + numberRef.value,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  state.conversation = response;
};
const openmodal = ref(false);
</script>
<template>
  <div class="header" v-if="state.user && state.user.ref">
    <div class="user-img">
      <img
        class="dp"
        :src="state.user.picture"
        :alt="state.user.name"
        @click="openmodal = !openmodal"
      />
    </div>
    <div class="nav-icons">
      <li><i class="fa-solid fa-users"></i></li>
      <li>
        <i class="fa-solid fa-message" @click="showModal = !showModal"> </i>
      </li>
      <li><i class="fa-solid fa-ellipsis-vertical"></i></li>
    </div>
  </div>
  <Modal v-if="showModal" @close="showModal = false">
    <template class="col center">
      <label for="number">Number:</label>
      <input
        type="text"
        id="number"
        name="number"
        input-text
        v-model="numberRef"
      /><br /><br />
    </template>
    <button @click="dofetch()" btn-get>Add Contact</button>
  </Modal>
  <Modal v-if="openmodal" @close="openmodal = false">
    <template #header>
      <h3>Contact Details</h3>
    </template>
    <template #default>
      <p><b>Number</b> : {{ state.user.ref }}</p>
    </template>
    <template #footer>
      <button @click="logout()" btn-del>Logout</button>
    </template>
  </Modal>
</template>
