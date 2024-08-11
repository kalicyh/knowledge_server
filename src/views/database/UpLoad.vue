<script setup lang="ts">
import { ref } from 'vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import UpLoad from '@/components/shared/WidgetUpLoad.vue';
</script>
<template>
    <v-row>
        <v-col cols="12" md="12">
            <UiParentCard title="数据上传"> 
                <UpLoad/>
            </UiParentCard>
        </v-col>
    </v-row>
</template>
