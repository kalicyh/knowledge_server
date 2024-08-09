<template>
  <h1>果之都智库</h1>
  <a>{{ version }}</a>
  <Copywriter/>
  <Contacts/>
</template>

<script>
import Contacts from './components/ContactsView/ContactsView.vue'
import Copywriter from './components/CopywriterView/CopywriterView.vue'
import { fetchInfo } from '@/utils/api';

export default {
  name: 'App',
  components: {
    Copywriter,
    Contacts
  },
  data() {
    return {
      version: ''
    };
  },
  methods: {
    async fetchInfo() {
      try {
        const result = await fetchInfo('/info');
        this.version = result.backend_versions;
      } catch (error) {
        this.error = error.message;
      }
    },
  },
  created() {
    this.fetchInfo();
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
