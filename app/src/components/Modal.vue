<template>
  <transition name="modal">
    <div class="fixed z-10 inset-0 overflow-y-auto" @click.self="emit('close')">
      <div class="flex items-center justify-center">
        <div class="bg-white rounded-lg shadow-lg p-8">
          <div class="modal-header">
            <slot name="header">
              <!-- Default header content can be placed here -->
            </slot>
          </div>
          <div class="modal-body">
            <slot></slot>
          </div>
          <div class="modal-footer">
            <slot name="footer">
              <button class="btn-del" @click="emit('close')">Close</button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
const emit = defineEmits(["close"]);
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter,
.modal-leave-to

/* .modal-leave-active in <2.6 */ {
  opacity: 0;
}
</style>
