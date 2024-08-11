<script setup lang="ts">
import { ref } from 'vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import UpLoad from '@/components/shared/WidgetUpLoad.vue';
import { API_BASE_URL } from '@/utils/config';
const tp_upload = `${API_BASE_URL}/talking_points/upload`;
const tp_upload_over = `${API_BASE_URL}/talking_points/overwrite_upload`;
</script>
<template>
    <v-row>
        <v-col cols="12" md="12">
            <UiParentCard title="数据上传"> 
                <UpLoad :uploadURL="tp_upload" />
            </UiParentCard>
        </v-col>
    </v-row>
</template>
