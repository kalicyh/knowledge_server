<template>
    <div>
      <n-input
        v-model="versionTag"
        round
        placeholder="版本号"
        @change="versionChange"
      />
      
      <n-upload
        ref="upload"
        :action="currentUploadURL"
        :default-upload="false"
        multiple
        @change="handleChange"
      >
        <n-button>选择文件</n-button>
      </n-upload>
      <n-button
        :disabled="!fileListLength"
        style="margin-bottom: 12px"
        @click="handleClick"
      >
        上传文件
      </n-button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue'
  import { NUpload, NButton, NInput } from 'naive-ui';
  import type { UploadFileInfo, UploadInst } from 'naive-ui'
  
  export default defineComponent({
    props: {
      uploadURL: {
        type: String,
        required: true
      }
    },
    components: {
      NUpload,
      NButton,
      NInput
    },
    setup(props) {
      const versionTag = ref('')
      const fileListLengthRef = ref(0)
      const uploadRef = ref<UploadInst | null>(null)
      const currentUploadURL = ref(props.uploadURL)
  
      const handleChange = (options: { fileList: UploadFileInfo[] }) => {
        fileListLengthRef.value = options.fileList.length
      }
      
      const versionChange = (v: string) => {
        currentUploadURL.value = `${props.uploadURL}?tag=${v}`
        console.log(currentUploadURL.value)
      }
  
      const handleClick = (v: string) => {
        uploadRef.value?.submit()
      }
  
      return {
        versionTag,
        fileListLength: fileListLengthRef,
        upload: uploadRef,
        handleChange,
        versionChange,
        handleClick,
        currentUploadURL
      }
    }
  })
  </script>
  