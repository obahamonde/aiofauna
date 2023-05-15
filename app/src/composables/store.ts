import { defineStore, acceptHMRUpdate } from 'pinia'
import { reactive } from 'vue'

export const useStore = defineStore('whatsApp',()=>{
    const state = reactive({
        user: null as any,
        contact: null as any,
        messages: [] as any,
        contacts: [] as any,
        conversation: null as any,
        whispers: [] as any,
        notifications: [] as any,
    })

    return {
        state
    }
})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useStore, import.meta.hot))
}
