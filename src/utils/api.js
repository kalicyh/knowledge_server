import axiosInstance from '@/utils/axiosInstance';

// 获取 MySQL 数据
export async function fetchMySQLData(url) {
  try {
    const response = await axiosInstance.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching MySQL data:', error);
    throw new Error('Error fetching MySQL data: ' + error.message);
  }
}

// 获取信息
export async function fetchInfo(url) {
  try {
    const response = await axiosInstance.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching info data:', error);
    throw new Error('Error fetching info data: ' + error.message);
  }
}
