<script setup lang="ts">
import { ref } from 'vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import UpLoad from '@/components/shared/VersionUpLoad.vue';
import { API_BASE_URL } from '@/utils/config';
const upload = `${API_BASE_URL}/client-file-tag/`;
</script>
<template>
    <v-row>
        <v-col cols="12" md="12">
            <UiParentCard title="管理版本">
                <UpLoad :uploadURL="upload" />
            </UiParentCard>
        </v-col>
    </v-row>
</template>
