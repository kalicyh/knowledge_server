import axiosInstance from '@/utils/axiosInstance';
import * as XLSX from 'xlsx';

// 处理文件上传
export function handleFileUpload(file, callback) {
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const workbook = XLSX.read(e.target.result, { type: 'array' });
      const worksheet = workbook.Sheets[workbook.SheetNames[0]];
      const data = XLSX.utils.sheet_to_json(worksheet);
      callback(data);
    };
    reader.readAsArrayBuffer(file);
  }
}

// 上传数据并轮询进度
export async function uploadData(file, uploadUrl, progressUrl, onProgress, onComplete) {
  if (!file) {
    throw new Error('未提供文件');
  }

  try {
    // 创建 FormData 并附加文件
    const formData = new FormData();
    formData.append('file', file);

    // 将文件发送到上传端点
    const response = await axiosInstance.post(uploadUrl, formData);
    const uploadId = response.data.upload_id;

    // 定期轮询进度更新
    const interval = setInterval(async () => {
      try {
        const progressResponse = await axiosInstance.get(`${progressUrl}/${uploadId}`);
        const progress = progressResponse.data.progress;

        if (onProgress) {
          onProgress(progress); // 通知进度
        }

        if (progress === 100) {
          clearInterval(interval);
          if (onComplete) {
            await onComplete(); // 完成后执行的操作
          }
        }
      } catch (error) {
        clearInterval(interval);
        throw new Error(`获取进度错误: ${error.message}`);
      }
    }, 1000); // 每秒轮询一次

  } catch (error) {
    throw new Error(`上传错误: ${error.message}`);
  }
}

// 获取信息并导出
export const getInfo = async () => {
  try {
    const result = await fetchInfo('/info');
    return result.backend_versions;
  } catch (error) {
    console.error(error.message);
    throw new Error(`获取信息错误: ${error.message}`);
  }
};
