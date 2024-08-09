<script setup lang="ts">
import { ref } from 'vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
</script>
<template>
    <v-row>
        <v-col cols="12" md="12">
            <UiParentCard title="数据库内容"> 
                <div class="pa-7 pt-1"><p class="text-body-1">content</p></div>
            </UiParentCard>
        </v-col>
    </v-row>
</template>
