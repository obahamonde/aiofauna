<script setup lang="ts">
import { useRequest } from "~/composables/request"
const { request, response, iserror, isloading } = useRequest()
const props = defineProps(
    {
        url: {
            type: String,
            required: true
        },
        options: {
            type: Object,
            required: false,
            default: () => ({
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            })
        }
    }
)
const { state } = useStore();
onMounted(async () => {
    await request(props.url, props.options);
});

watchEffect(() => {
    if (iserror.value) {
        state.notifications.push({
            status: 'error',
            message: typeof iserror.value === 'string' ? iserror.value : JSON.stringify(iserror.value)
        });
    }
});

const loaderActive = computed(() => isloading.value);
</script>
<template>
    <div v-if="!iserror && !loaderActive && response">
        <slot :response="response"></slot>
    </div>
    <div v-else-if="iserror">
        <slot name="error" :error="iserror">
            <!-- Add default error handling UI here -->
            <p>An error occurred: {{ iserror.message }}</p>
        </slot>
    </div>
    <div v-else-if="loaderActive">
        <slot name="loading">
            <Icon icon="mdi-loading" animate-spin x2 />
        </slot>
    </div>
</template>