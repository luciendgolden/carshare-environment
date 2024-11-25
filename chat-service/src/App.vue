<template>
  <v-app>
    <v-main>
      <v-container fluid class="primary bg-blue">
        <v-row justify="center">
          <v-col xl="6" sm="12">
            <chat-window />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import ChatWindow from './components/ChatWindow.vue';

export default {
  name: 'App',
  components: {
    ChatWindow
  },
}
</script>