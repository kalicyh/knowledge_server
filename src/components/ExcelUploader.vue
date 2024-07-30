<template>
  <div>
    <input type="file" @change="handleFileUpload" />
    <button @click="togglePreviewData">{{ showPreviewData ? '隐藏上传文件数据' : '预览上传文件' }}</button>
    <button @click="toggleFetchMySQLData">{{ showFetchMySQLData ? '隐藏数据库内容' : '预览数据库内容' }}</button>
    <button @click="uploadData">新增数据</button>
    <button @click="uploadnewData">覆盖数据</button>

    <!-- Preview for uploaded file -->
    <div v-if="showPreviewData">
      <h2>上传文件数据预览</h2>
      <table>
        <thead>
          <tr>
            <th>名字</th>
            <th>分类</th>
            <th>文案</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in data" :key="index">
            <td>{{ item.名字 }}</td>
            <td>{{ item.分类 }}</td>
            <td>{{ item.文案 }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Preview for MySQL data -->
    <div v-if="showFetchMySQLData">
      <h2>数据库内容预览</h2>
      <table>
        <thead>
          <tr>
            <th>序号</th>
            <th>名字</th>
            <th>分类</th>
            <th>文案</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in mysqlData" :key="item.序号">
            <td>{{ item.序号 }}</td>
            <td>{{ item.名字 }}</td>
            <td>{{ item.分类 }}</td>
            <td>{{ item.文案 }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="progress >= 0">
      <p>Progress: {{ progress }}%</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as XLSX from 'xlsx';

export default {
  data() {
    return {
      file: null,
      data: [],
      mysqlData: [],
      error: null,
      progress: -1, // Initialize progress
      showPreviewData: false,
      showFetchMySQLData: false,
      uploadId: null // Track upload session
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.file = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          const workbook = XLSX.read(e.target.result, { type: 'array' });
          const worksheet = workbook.Sheets[workbook.SheetNames[0]];
          this.data = XLSX.utils.sheet_to_json(worksheet);
        };
        reader.readAsArrayBuffer(file);
      }
    },
    async previewData() {
      console.log(this.data);
    },
    async fetchMySQLData() {
      try {
        const response = await axios.get('/data');
        this.mysqlData = response.data.records;
      } catch (error) {
        console.error('Error fetching MySQL data:', error);
        this.error = 'Error fetching MySQL data: ' + error.message;
      }
    },
    togglePreviewData() {
      this.showPreviewData = !this.showPreviewData;
      this.showFetchMySQLData = false;
      if (this.showPreviewData) {
        this.previewData();
      }
    },
    toggleFetchMySQLData() {
      this.showFetchMySQLData = !this.showFetchMySQLData;
      this.showPreviewData = false;
      if (this.showFetchMySQLData) {
        this.fetchMySQLData();
      }
    },
    async uploadData() {
      if (this.file) {
        try {
          const formData = new FormData();
          formData.append('file', this.file);

          // Post file to upload endpoint
          const response = await axios.post('/upload', formData);
          this.uploadId = response.data.upload_id;

          // Poll for progress updates
          const interval = setInterval(async () => {
            try {
              const progressResponse = await axios.get(`/progress/${this.uploadId}`);
              this.progress = progressResponse.data.progress;

              if (this.progress === 100) {
                clearInterval(interval);
              }
            } catch (error) {
              clearInterval(interval);
              console.error('Error fetching progress:', error);
              this.error = 'Error fetching progress: ' + error.message;
            }
          }, 1000); // Poll every second

        } catch (error) {
          console.error('Upload error:', error);
          this.error = 'Upload error: ' + error.message;
        }
      } else {
        alert('Please select a file to upload.');
      }
    },
    async uploadnewData() {
      if (this.file) {
        try {
          const formData = new FormData();
          formData.append('file', this.file);

          // Post file to upload endpoint
          const response = await axios.post('/overwrite_upload', formData);
          this.uploadId = response.data.upload_id;

          // Poll for progress updates
          const interval = setInterval(async () => {
            try {
              const progressResponse = await axios.get(`/progress/${this.uploadId}`);
              this.progress = progressResponse.data.progress;

              if (this.progress === 100) {
                clearInterval(interval);
              }
            } catch (error) {
              clearInterval(interval);
              console.error('Error fetching progress:', error);
              this.error = 'Error fetching progress: ' + error.message;
            }
          }, 1000); // Poll every second

        } catch (error) {
          console.error('Upload error:', error);
          this.error = 'Upload error: ' + error.message;
        }
      } else {
        alert('Please select a file to upload.');
      }
    }
  }
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
