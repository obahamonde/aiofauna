<script setup lang="ts">
type Upload = {
  ref: string | undefined;
  ts: string | undefined;
  user: string;
  name: string;
  key: string;
  size: number;
  type: string;
  lastModified: number;
  url: string;
};

const filesData = reactive<any[]>([]);
const filesUpload = reactive<Upload[]>([]);
const { state } = useStore();

const getFiles = async () => {
  const { data } = await useFetch(`/api/upload?user=${state.user.ref}`, {
    method: "GET",
  }).json();
  const files = unref(data);
  files.forEach((file: any) => {
    filesUpload.push(file);
  });
};

const onDrop = async (files: File[] | null) => {
  if (!files || files.length === 0) return;
  files
    .map((file) => {
      const url = useObjectUrl(file);
      return {
        user: state.user.ref as string,
        name: file.name,
        key: state.user.ref as string,
        url: url.value,
        type: file.type,
        lastModified: file.lastModified,
        file: file,
      };
    })
    .forEach(async (file) => {
      filesData.push(file);
      const formData = new FormData();
      formData.append("file", file.file);
      const { data } = await useFetch(
        `/api/upload?key=${file.key}&size=${file.file.size}&user=${file.user}`,
        {
          method: "POST",
          body: formData,
        }
      ).json();
      filesUpload.push(unref(data));
    });
  await getFiles();
};
const dropZoneRef = ref<HTMLElement>();

const { isOverDropZone } = useDropZone(dropZoneRef, onDrop);

const useInputEl = () => {
  const el = document.createElement("input");
  el.onchange = (e) => {
    const files = (e.target as HTMLInputElement).files as FileList;
    onDrop(Array.from(files));
  };
  el.setAttribute("type", "file");
  el.setAttribute("multiple", "true");
  el.setAttribute("accept", "*/*");
  el.click();
};

const deleteFile = async (file: any) => {
  await useFetch(`/api/upload?ref=${file.ref}`, {
    method: "DELETE",
  }).json();
  filesData.splice(filesData.indexOf(file), 1);
  filesUpload.splice(filesUpload.indexOf(file), 1);
  await getFiles();
  state.notifications.push({
    status: "success",
    message: "File deleted",
  });
};

onMounted(async () => {
  if (!state.user) return;
  await getFiles();
});
</script>

<template>
  <div class="flex gap-4 max-h-400px">
    <div class="w-full relative rounded-lg sh">
      <div
        ref="dropZoneRef"
        @click="useInputEl"
        multiple
        class="flex flex-col w-full min-h-200px h-auto bg-gray-400/10 justify-center items-center mt-6"
      >
        <div>
          {{ isOverDropZone ? "Drop here" : "Drag and drop files here" }}
        </div>
      </div>
      <div class="col center m-8">
        <div class="grid3 p-8 gap-8">
          <div
            v-for="(file, index) in filesUpload"
            :key="index"
            class="col bg-gray-100 sh center gap-2 p-4"
          >
            <p class="row gap-4">
              <Icon
                icon="mdi-close"
                @click="deleteFile(file)"
                class="x2 cp hover:red-700 text-red-500 scale"
              />
            </p>
            <p class="text-sm text-body">{{ file.name }}</p>
            <p class="text-sm text-body">
              {{ (file.size / 1000).toFixed(2) }} Kb
            </p>
            <p class="text-sm text-body">{{ file.type }}</p>
            <p class="text-sm text-body">
              {{ new Date(file.lastModified).toLocaleString() }}
            </p>

            <div class="col center p-8">
              <div v-if="file.type.includes('image')">
                <a :href="file.url" target="_blank"> <img :src="file.url" /></a>
              </div>
              <div v-else-if="file.type.includes('video')">
                <video controls :src="file.url" />
                <a :href="file.url" target="_blank">
                  <Icon icon="mdi-video" class="x4" />
                </a>
              </div>
              <div v-else-if="file.type.includes('audio')">
                <a :href="file.url" target="_blank">
                  <Icon icon="mdi-music" class="x4" />
                </a>
                <audio controls :src="file.url" />
              </div>
              <div v-else>
                <a :href="file.url" target="_blank">
                  <Icon icon="mdi-file" class="x4" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
