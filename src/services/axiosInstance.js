import axios from 'axios';

// 从环境变量中获取 baseURL
const baseURL = process.env.VUE_APP_BASE_URL;

// 创建 Axios 实例，并设置 baseURL
const instance = axios.create({
  baseURL: baseURL
});

export default instance;
