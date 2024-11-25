<template>
  <div class="chat-window">
    <v-card class="text-start">
      <v-card-title class="headline">
        <v-list-item title="Car2Go" subtitle="Active now 🟢">
          <template v-slot:prepend>
            <v-avatar color="grey-lighten-1">
              <v-img cover src="@/assets/car.jpg"></v-img>
            </v-avatar>
          </template>
        </v-list-item>
      </v-card-title>
      <v-divider></v-divider>


      <v-card-text>
        <div class="messages">
          <transition-group name="list" tag="ul">
            <message v-for="(message, index) in messages" :key="index" :message="message" />
          </transition-group>
          <message v-if="isLoading" :isLoading="true" :message="{ text: '...', from: 'car' }" />
        </div>
      </v-card-text>
      <v-card-actions>
        <v-col cols="2">
          <v-autocomplete v-model="selectedCar" :items="carList" color="success" label="Select a Car">
            <template v-slot:chip="{ props, item }">
              <v-chip v-bind="props" :prepend-icon="'mdi mdi-car'" :text="item.title"></v-chip>
            </template>
          </v-autocomplete>
        </v-col>
        <v-menu open-on-click>
          <template v-slot:activator="{ props }">
            <v-text-field v-model="newMessage" :clearable="true" variant="outlined" @keyup.enter="sendMessage"
              v-bind="props" placeholder="Type a message..."></v-text-field>
          </template>

          <v-list class="messages">
            <message class="clickable" v-for="(message, index) in preDefinedMessages" :key="index" :message="message"
              @click="handleItemClick(message)" />
          </v-list>
        </v-menu>

        <v-btn @click="sendMessage" icon>
          <v-icon>mdi-send</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>


<script>
import axios from 'axios';
import Message from "@/components/Message.vue";

export default {
  components: {
    Message,
  },
  mounted() {
    this.getCarListApiCall()
  },
  beforeMount() {
    this.setPredefinedQuestions()
  },
  data() {
    return {
      isLoading: false,
      messages: [
        { text: "Hello! Need a ride? Let's talk aobut it.", from: "car" },
        { text: "You can always select nearby cars from left-bottom dropdown and ask any question related to your trip. ;)", from: "car" },
      ],
      preDefinedMessages: [],
      newMessage: "",
      carList: [],
      selectedCar: null
    };
  },
  methods: {
    setPredefinedQuestions() {
      this.preDefinedMessages = [
        { text: "What is the type of " + this.selectedCar + "?", from: "user" },
        { text: "What is the model of " + this.selectedCar + "?", from: "user" },
        { text: "What is the recommended action for the weather in Vienna?", from: "user" },
        { text: "Is the " + this.selectedCar + " available?", from: "user" },
        { text: "What is the condition of " + this.selectedCar + "?", from: "user" },
        { text: "What is the TransmissionsType of the " + this.selectedCar + "?", from: "user" },
        { text: "What is the PricePerKM for " + this.selectedCar + "?", from: "user" },
        { text: "Can you summarize me information about " + this.selectedCar + "?", from: "user" }
      ]
    },
    sendMessage() {
      if (this.newMessage.trim() !== "") {
        this.postQuestionApiCall();
      }
    },
    handleItemClick(item) {
      this.newMessage = item.text;
      this.postQuestionApiCall();
    },
    replyFromCar(message) {
      setTimeout(() => {
        this.messages.push({ text: message, from: "car" });
      }, 1000);
    },
    async getCarListApiCall() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/get-car-list');
        let carList = response?.data?.carList ?? [];
        carList.push("General")
        this.carList = carList;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    async postQuestionApiCall() {
      this.messages.push({ text: this.newMessage, from: "user" });
      this.isLoading = true;
      try {
        const requestBody = {
          question: this.newMessage,
          carId: this.selectedCar == "General" ? null : this.selectedCar
        };
        const response = await axios.post('http://127.0.0.1:8000/question', requestBody);
        this.isLoading = false;
        const replyText = response.data.answer;
        this.replyFromCar(replyText);
        this.newMessage = "";
      } catch (error) {
        console.error('Error fetching data:', error);
        this.isLoading = false;
        this.replyFromCar(error);
      }
    }

  },
  watch: {
    selectedCar(val) {
      if (val != "General") {
        this.messages.push({ text: "Hello! I'm " + this.selectedCar + ". How can I help you?", from: "car" });
        this.setPredefinedQuestions()
      }
    }
  }
};
</script>

<style scoped>
/* .chat-window {
  width: 600px;
} */

.messages {
  height: 70vh;
  overflow-y: auto;
}

.message-user {
  text-align: right;
}

.message-car {
  text-align: left;
}

.v-avatar {
  margin-right: 10px;
}

/* .clickable {
  cursor: pointer;
} */
.clickable:hover {
  cursor: pointer;

}

.messages {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.messages::-webkit-scrollbar {
  display: none;
}

.chat-window {
  height: 100vh;
}


.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>
