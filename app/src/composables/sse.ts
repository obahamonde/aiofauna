export const useSSE = (props: { url: string; query: string }) => {
  const { status, data, eventSource, close } = useEventSource(
    `${props.url}?ref=${props.query}`
  );

  const messages = ref<any[]>([]);

  watch(data, (newData) => {
    if (newData) {
      messages.value.push(JSON.parse(newData));
    }
  });

  onUnmounted(() => {
    close();
  });

  return {
    messages,
    status,
    eventSource,
  };
};
