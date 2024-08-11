import axios from 'axios';
import axiosRetry from 'axios-retry';
import { API_BASE_URL } from '@/utils/config';

const instance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000, // 可选的请求超时设置
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器
instance.interceptors.request.use(
    (config) => {
        // 可以在这里添加请求拦截器
        // 比如添加认证 token
        // const token = localStorage.getItem('token');
        // if (token) {
        //     config.headers.Authorization = `Bearer ${token}`;
        // }
        return config;
    },
    (error) => {
        // 请求错误处理
        return Promise.reject(error);
    }
);

// 响应拦截器
instance.interceptors.response.use(
    (response) => response,
    (error) => {
        // 响应错误处理
        if (axios.isAxiosError(error)) {
            if (error.response) {
                // 处理 HTTP 状态码
                const status = error.response.status;
                switch (status) {
                    case 400:
                        console.error('Bad Request: The server could not understand the request.');
                        break;
                    case 401:
                        console.error('Unauthorized: Authentication is required or has failed.');
                        break;
                    case 403:
                        console.error('Forbidden: You do not have permission to access this resource.');
                        break;
                    case 404:
                        console.error('Not Found: The requested resource could not be found.');
                        break;
                    case 500:
                        console.error('Internal Server Error: An error occurred on the server.');
                        break;
                    default:
                        console.error(`Unexpected error: ${status}`);
                        break;
                }
            } else {
                // 请求错误（没有响应）
                console.error('Network error or CORS issue:', error.message);
            }
        } else {
            // 非 Axios 错误
            console.error('Unexpected error:', error);
        }

        return Promise.reject(error);
    }
);

// 请求重试机制
axiosRetry(instance, { retries: 3, retryDelay: axiosRetry.exponentialDelay });

export const fetchData = async <T>(url: string, config: any = {}): Promise<T> => {
    try {
        const response = await instance.get<T>(url, config);
        return response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error; // 将错误重新抛出以便在调用处处理
    }
};

// 取消请求的示例
const cancelTokenSource = axios.CancelToken.source();

export const cancelRequest = () => {
    cancelTokenSource.cancel('Operation canceled by the user.');
};

export default instance;
