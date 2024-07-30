<template>
  <div>
    <input type="file" @change="handleFileUpload" />
    <button @click="previewData">预览数据</button>
    <button @click="uploadData">上传数据</button>
    
    <!-- Progress Bar -->
    <div v-if="progress > 0">
      <p>上传进度: {{ progress }}%</p>
      <progress :value="progress" max="100"></progress>
    </div>
    
    <div v-if="data.length">
      <h2>数据预览</h2>
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
          <tr v-for="item in data" :key="item.序号">
            <td>{{ item.序号 }}</td>
            <td>{{ item.名字 }}</td>
            <td>{{ item.分类 }}</td>
            <td>{{ item.文案 }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="mysqlData.length">
      <h2>MySQL 数据库内容</h2>
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
      progress: 0
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
          const worksheet = workbook.Sheets[workbook.sheetNames[0]];
          this.data = XLSX.utils.sheet_to_json(worksheet);
        };
        reader.readAsArrayBuffer(file);
      }
    },
    async previewData() {
      // Show preview data
      console.log(this.data);
    },
    async uploadData() {
      if (this.file) {
        try {
          const formData = new FormData();
          formData.append('file', this.file);

          await axios.post('http://localhost:8000/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: (progressEvent) => {
              this.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            }
          });
          
          // Reset progress after upload
          this.progress = 0;
        } catch (err) {
          this.error = '文件上传失败，请检查网络连接或服务器状态。';
          console.error(err);
        }
      }
    },
    async fetchMySQLData() {
      try {
        const response = await axios.get('http://localhost:8000/data');
        this.mysqlData = response.data.records;
      } catch (err) {
        this.error = '获取数据库数据失败，请检查网络连接或服务器状态。';
        console.error(err);
      }
    }
  },
  mounted() {
    this.fetchMySQLData();
  }
};
</script>

<style>
.error {
  color: red;
  font-weight: bold;
}
</style>
