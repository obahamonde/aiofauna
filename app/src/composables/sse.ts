export const useSSE = (props:{url:string, refParam:string}) => {


  const { status, data, eventSource, close } = useEventSource(`${props.url}?ref=${props.refParam}`);

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
    eventSource
  };
};
