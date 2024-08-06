<template>
  <h1>果之都智库</h1>
  <ExcelUploader/>
  <ContactPerson/>
</template>

<script>
import ContactPerson from './components/ContactPerson.vue'
import ExcelUploader from './components/ExcelUploader.vue'

export default {
  name: 'App',
  components: {
    ExcelUploader,
    ContactPerson
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
