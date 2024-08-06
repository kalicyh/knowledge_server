<template>
  <div>
    <p>数据条数: {{ totalRows }}</p>
    <p>最后更新: {{ lastUpdated }}</p>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="progress >= 0">
      <p>进度: {{ progress }}%</p>
    </div>

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
            <td>{{ item.月份 }}</td>
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
            <th>月份</th>
            <th>分类</th>
            <th>文案</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in mysqlData" :key="item.序号">
            <td>{{ item.序号 }}</td>
            <td>{{ item.名字 }}</td>
            <td>{{ item.月份 }}</td>
            <td>{{ item.分类 }}</td>
            <td>{{ item.文案 }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { handleFileUpload, uploadData } from '@/utils/utils';
import { fetchMySQLData, fetchInfo } from '@/utils/api';

export default {
  data() {
    return {
      file: null,
      data: [],
      mysqlData: [],
      error: null,
      progress: -1,
      showPreviewData: false,
      showFetchMySQLData: false,
      lastUpdated: '',
      totalRows: 0
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.file = file;
        handleFileUpload(file, (data) => {
          this.data = data;
        });
      }
    },
    async fetchMySQLData() {
      try {
        const result = await fetchMySQLData('/talking_points/data');
        this.mysqlData = result.records;
      } catch (error) {
        this.error = error.message;
      }
    },
    async fetchInfo() {
      try {
        const result = await fetchInfo('/talking_points/info');
        this.lastUpdated = result.last_updated;
        this.totalRows = result.total_rows;
      } catch (error) {
        this.error = error.message;
      }
    },
    togglePreviewData() {
      this.showPreviewData = !this.showPreviewData;
      this.showFetchMySQLData = false;
    },
    toggleFetchMySQLData() {
      this.showFetchMySQLData = !this.showFetchMySQLData;
      this.showPreviewData = false;
      if (this.showFetchMySQLData) {
        this.fetchMySQLData();
      }
    },
    async uploadData() {
      try {
        await uploadData(this.file, '/talking_points/upload', '/talking_points/progress', (progress) => {
          this.progress = progress; // 更新进度状态
        }, async () => {
          await this.fetchInfo(); // 上传完成后获取更新的信息
        });
      } catch (error) {
        this.error = error.message;
        console.error('上传错误:', error);
      }
    },
    async uploadnewData() {
      try {
        await uploadData(this.file, '/talking_points/overwrite_upload', '/talking_points/progress', (progress) => {
          this.progress = progress; // 更新进度状态
        }, async () => {
          await this.fetchInfo(); // 上传完成后获取更新的信息
        });
      } catch (error) {
        this.error = error.message;
        console.error('上传错误:', error);
      }
    }
  },
  created() {
    this.fetchInfo(); // 组件创建时获取初始信息
  }
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
