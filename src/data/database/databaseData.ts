import axios from '@/utils/axios'; // 引入配置好的 axios 实例
import type { productPerformanceType } from '@/types/database/index';
import { PUBLIC_PATH } from '@/utils/config';

// 定义响应数据的接口
interface ProductPerformanceResponse {
    total_records: number;
    records: productPerformanceType[];
}

export const fetchProductPerformance = async (): Promise<productPerformanceType[]> => {
    try {
        const response = await axios.get<ProductPerformanceResponse>(`${PUBLIC_PATH}/talking_points/data`);
        return response.data.records;
    } catch (error) {
        console.error('Error fetching product performance:', error);
        return [];
    }
};
