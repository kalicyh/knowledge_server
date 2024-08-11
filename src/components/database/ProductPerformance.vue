<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { fetchProductPerformance } from '@/data/database/databaseData';
import type { productPerformanceType } from '@/types/database/index';

const allData = ref<productPerformanceType[]>([]);
const loading = ref(true);
const currentPage = ref(1);
const pageSize = 10;

// 计算当前页的数据
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return allData.value.slice(start, end);
});

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(allData.value.length / pageSize);
});

const loadData = async () => {
  loading.value = true;
  try {
    const response = await fetchProductPerformance();
    allData.value = response;
  } catch (error) {
    console.error('Error fetching product performance:', error);
  } finally {
    loading.value = false;
  }
};

// 在组件挂载后加载数据
onMounted(() => {
  loadData();
});
</script>

<template>
  <v-card elevation="10">
    <v-card-item class="pa-6">
      <v-card-title class="text-h5 pt-sm-2 pb-7">数据库内容</v-card-title>
      <v-table class="month-table">
        <thead>
          <tr>
            <th class="text-subtitle-1 font-weight-bold">序号</th>
            <th class="text-subtitle-1 font-weight-bold">名字</th>
            <th class="text-subtitle-1 font-weight-bold">月份</th>
            <th class="text-subtitle-1 font-weight-bold">分类</th>
            <th class="text-subtitle-1 font-weight-bold">文案</th>
          </tr>
        </thead>
        <tbody>
          <!-- 显示加载中的内容 -->
          <tr v-if="loading">
            <td colspan="5" class="text-center">加载中...</td>
          </tr>
          <!-- 显示数据 -->
          <tr v-else-if="paginatedData.length > 0" v-for="(item, index) in paginatedData" :key="item.序号" class="month-item">
            <td>
              <p class="text-15 font-weight-medium">{{ (currentPage - 1) * pageSize + index + 1 }}</p>
            </td>
            <td>
              <div>
                <h6 class="text-subtitle-1 font-weight-bold">{{ item.名字 }}</h6>
              </div>
            </td>
            <td>
                <h6 class="text-body-1 text-muted">{{ item.月份 }}</h6>
            </td>
            <td>
                <h6 class="text-body-1 text-muted">{{ item.分类 }}</h6>
            </td>
            <td>
              <h6 class="text-h6">{{ item.文案 }}</h6>
            </td>
          </tr>
          <!-- 显示暂无数据的内容 -->
          <tr v-else>
            <td colspan="5" class="text-center">暂无数据</td>
          </tr>
        </tbody>
      </v-table>
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        class="my-4"
      />
    </v-card-item>
  </v-card>
</template>
