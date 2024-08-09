<script setup lang="ts">
import { ref } from 'vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import ProductPerformance from '@/components/database/ProductPerformance.vue';
</script>
<template>
    <v-row>
        <v-col cols="12" md="12">
            <ProductPerformance />
        </v-col>
    </v-row>
</template>
