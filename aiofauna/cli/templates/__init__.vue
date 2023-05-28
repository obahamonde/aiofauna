<script setup lang="ts">
  #{ if in == 'query' }
const @{ name } = ref < @{ type } > (@{ default });
  #{ else }
const @{ name } = ref < @{ type } > (@{ default });
  #{ endif }

  #{ if body }
  export interface @{ body.content['application/json'].schema.title } {
    #{ for k, v in body.content['application/json'].schema.properties.items() }
  @{ k }: @{ v.type };
    #{ endfor }
}
  #{ endif }

const url = computed(() => {
  let url = '@{ path }' + '?' + @{ params }.map(p => p.name + '=' + p.value).join('&');
  return url;
});

const trigger = ref(false);
</script>

<template>
  <Request method="@{ method }" :url="url" :headers="headers" :body="body" v-if="trigger">
    <slot :json="{ json }"></slot>

    <slot #actions="{ json }">
      <button @click="trigger = !trigger">Send</button>
    </slot>

    <slot #error="{ json }">
      <div v-if="json.error">
        <h3>Error</h3>
        <pre>{{ json.error }}</pre>
      </div>
    </slot>
  </Request>
</template>
