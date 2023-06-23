<script setup lang="ts">
const { state } = useStore();
const process = (a: any) => {
  let els = []
  for (let i = 0; i < a.length; i++) {
    const el = JSON.parse(a[i])
    if (el.ref == state.user.ref) {
      continue
    }
    els.push(el)
  }
  return els
}
const handleClick = (ref_: string) => {
  alert(ref_)
}


</script>
<template>
  <Modal @close="$emit('close')" class="col center">

    <Request url="/api/users" class="col center px-4 gap-4">
      <template #="{ json }">
        <section class=" mb-4 col">
          <h1 class="m-4 font-extrabold">Click the picture to send Invitation</h1>
          <div v-for="item in process(json)" class="row start my-2 gap-4">
            <img :src="item.picture" class="x4 rf sh cp scale " @click="handleClick(item.ref)" />
            <div class="col start">
              <h3 class="text-body">{{ item.name }}</h3>
              <p class="text-caption">{{ item.ref }}</p>
            </div>
          </div>
        </section>
      </template>
    </Request>
  </Modal>
</template>