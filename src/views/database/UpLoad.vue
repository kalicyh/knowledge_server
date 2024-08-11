<script setup lang="ts">
import { ref, computed } from 'vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import UpLoad from '@/components/shared/WidgetUpLoad.vue';
import { API_BASE_URL } from '@/utils/config';

const tp_upload = `${API_BASE_URL}/talking_points/upload`;
const tp_upload_over = `${API_BASE_URL}/talking_points/overwrite_upload`;
const tp_selectedTab = ref('upload');
const tp_uploadURL = computed(() => {
  return tp_selectedTab.value === 'upload' ? tp_upload : tp_upload_over;
});

const n_upload = `${API_BASE_URL}/numbers/upload`;
const n_upload_over = `${API_BASE_URL}/numbers/overwrite_upload`;
const n_selectedTab = ref('upload');
const n_uploadURL = computed(() => {
  return n_selectedTab.value === 'upload' ? n_upload : n_upload_over;
});
</script>

<template>
  <v-row>
    <v-col cols="12" md="12">
      <UiParentCard title="语料数据上传">
        <v-tabs v-model="tp_selectedTab" background-color="transparent">
          <v-tab value="upload">新增</v-tab>
          <v-tab value="overwrite">覆盖</v-tab>
        </v-tabs>

        <UpLoad :uploadURL="tp_uploadURL" />
      </UiParentCard>
    </v-col>
    <v-col cols="12" md="12">
      <UiParentCard title="号码数据上传">
        <v-tabs v-model="n_selectedTab" background-color="transparent">
          <v-tab value="upload">新增</v-tab>
          <v-tab value="overwrite">覆盖</v-tab>
        </v-tabs>

        <UpLoad :uploadURL="n_uploadURL" />
      </UiParentCard>
    </v-col>
  </v-row>
</template>
