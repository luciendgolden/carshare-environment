<!-- components/Message.vue -->
<template>
  <v-row :justify="message.from === 'user' ? 'end' : 'start'">
    <v-col v-if="message.from !== 'user'" cols="auto">
      <v-avatar color="grey-lighten-1" class="border">
        <v-img cover src="@/assets/car.jpg"></v-img>
      </v-avatar>
    </v-col>
    <v-col cols="6">
      <v-progress-linear v-if="isLoading" :height="32" color="green" indeterminate rounded height="6"></v-progress-linear>
      <div v-else :class="(message.from === 'user' ? 'message-user' : 'message-other') +' message-text'">
        {{ message.text }}
      </div>
    </v-col>
    <v-col v-if="message.from === 'user'" cols="auto">
      <v-avatar color="grey-lighten-1" class="border">
        <v-img cover src="@/assets/user.png"></v-img>
      </v-avatar>
    </v-col>

  </v-row>
</template>
  
<script>
export default {
  props: {
    isLoading: false,
    message: {
      type: Object,
      required: true,
    },
  },
};
</script>
  
<style scoped>
.message-user {
  background-color: #4caf50;
  color: white;
  padding: 8px;
  margin: 5px;
  border-radius: 10px;
  align-self: flex-end;
}

.message-other {
  background-color: #e0e0e0;
  padding: 8px;
  margin: 5px;
  border-radius: 10px;
}


.message-text:hover{
  background: #00723d;
}

</style>
  