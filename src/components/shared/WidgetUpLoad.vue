<template>
  <n-upload multiple directory-dnd :action="$props.uploadURL" @before-upload="beforeUpload" :max="5">
    <n-upload-dragger>
      <div style="margin-bottom: 12px">
        <n-icon size="48" :depth="3">
          <ArchiveIcon />
        </n-icon>
      </div>
      <n-text style="font-size: 16px">
        点击或者拖动文件到该区域来上传
      </n-text>
      <n-p depth="3" style="margin: 8px 0 0 0">
        请不要上传敏感数据，比如你的银行卡号和密码，信用卡号有效期和安全码
      </n-p>
    </n-upload-dragger>
  </n-upload>
</template>

<script lang="ts">
import { defineComponent,type PropType } from 'vue';
import { NUpload, NUploadDragger, NIcon, NP, NText, useMessage } from 'naive-ui';
import type { UploadFileInfo } from 'naive-ui'

export default defineComponent({
  setup() {
    const message = useMessage()
    return {
      async beforeUpload(data: {
        file: UploadFileInfo
        fileList: UploadFileInfo[]
      }) {
        if (data.file.file?.type !== 'xlsx') {
          message.error('只能上传xlsx格式的文件，请重新上传')
          return false
        }
        return true
      }
    }
  },
  components: {
    NUpload,
    NUploadDragger,
    NIcon,
    NP,
    NText
  },
  props: {
    uploadURL: {
      type: String as PropType<string>,
      required: true
    }
  }
});
</script>
