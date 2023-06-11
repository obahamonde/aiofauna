import { defineStore, acceptHMRUpdate } from "pinia";
import { reactive } from "vue";

type User = {
  ref: string;
  ts: string;
  email: string;
  email_verified: boolean;
  family_name: string;
  given_name: string;
  locale: string;
  name: string;
  nickname: string;
  picture: string;
  sub: string;
  updated_at: string;
  is_online: boolean;
};

export const useStore = defineStore("whatsApp", () => {
  const state = reactive({
    user: {} as User,
    conversation: null as any,
    notifications: [] as any,
  });

  return {
    state,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStore, import.meta.hot));
}
