<template>
  <h1>果之都智库</h1>
  <Copywriter/>
  <Contacts/>
</template>

<script>
import Contacts from './components/ContactsView/ContactsView.vue'
import Copywriter from './components/CopywriterView/CopywriterView.vue'

export default {
  name: 'App',
  components: {
    Copywriter,
    Contacts
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
