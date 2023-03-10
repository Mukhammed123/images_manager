<template>
  <div class="home">
    <div class="control-card">
      <div class="wrapper">
        <div class="action-container">
          <div class="action-block">
            <div class="upload-file" @click="openDialog"> {{ uploadTitle }} </div>
            <input type="file" name="" id="fileInput" hidden @input="uploadImage">
            <div class="filter-block">
              <span class="all-btn" @click="getAllPosts">All</span>
              <span class="start-range">
                <a-date-picker @change="getPosts" v-model:value="startDate" :disabledDate="disableStartDate" />
              </span>
              <span class="end-range">
                <a-date-picker @change="getPosts" v-model:value="endDate" :disabledDate="disableEndDate" />
              </span>
              <span>
                <input v-model="enteredLocation" type="text" class="search-location" placeholder="Search by location"
                  @input="getPosts" />
              </span>
            </div>
            <div class="search-block">
              <div class="input-container">
                <input v-model="searchPerson" class="search-input" type="text"
                  placeholder="Search pictures by people tagged on..." @input="getPeople" />
                <a-button type="primary" @click="getPosts">Search</a-button>
              </div>
            </div>
            <div class="name-options">
              <ul>
                <li v-for="(personName, nameIndex) in searchedPeople" :key="`${personName}-${nameIndex}`"
                  class="person-name" @click="nameClicked(personName)">
                  {{ personName }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        <PostBlocks :posts-data="postsData" />
      </div>
    </div>
    <PostImageDialogVue :key="dialogKey" :show-add-dialog="showAddDialog" @close="showAddDialog = false"
      @submit="getPosts()" />
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import PostImageDialogVue from '@/components/dialogs/PostImageDialog.vue';
import axios from 'axios';
import { useStore } from "@/stores/rootStore";
import PostBlocks from '@/components/PostBlocks.vue';
// import { Moment } from "moment";

export default defineComponent({
  name: "HomeView",
  components: { PostImageDialogVue, PostBlocks },
  setup() {
    const startDate = ref(undefined);
    const endDate = ref(undefined);
    const showAddDialog = ref(false);
    const dialogKey = ref(0);
    const uploadTitle = ref("Upload file");
    const store = useStore();
    const postsData = ref([]);
    const enteredLocation = ref(undefined);
    const searchPerson = ref(undefined);
    const searchedPeople = ref([]);

    onMounted(async () => {
      getPosts();
    })

    const getAllPosts = () => {
      enteredLocation.value = undefined;
      startDate.value = undefined;
      endDate.value = undefined;
      searchPerson.value = undefined;
      getPosts();
    }

    const getPeople = async () => {
      if ((searchPerson.value || '').length > 0) {
        const response = await axios.get("http://localhost:8000/api/images/people/", {
          headers: {
            "Authorization": store.accessToken
          },
          params: {
            starts_with: searchPerson.value
          }
        });
        searchedPeople.value = response.data.map(item => item.name);
      } else searchedPeople.value = [];
    }

    const getPosts = async () => {
      const response = await axios.get("http://localhost:8000/api/images/", {
        headers: {
          "Authorization": store.accessToken
        },
        params: {
          location: enteredLocation.value,
          start: startDate.value ? Math.floor(new Date(startDate.value) / 1000) : undefined,
          end: endDate.value ? Math.floor(new Date(endDate.value) / 1000) : undefined,
          person: searchPerson.value
        }
      });
      postsData.value = response.data;
    }

    const nameClicked = (name) => {
      searchPerson.value = name;
      searchedPeople.value = [];
    }

    const openDialog = () => {
      dialogKey.value += 1;
      showAddDialog.value = true;
    }

    const disableStartDate = (e) => new Date() < new Date(e.$d);

    const disableEndDate = (e) => startDate.value ? new Date(e.$d) < new Date(startDate.value) : false;

    const uploadImage = (e) => {
      console.log(e.target.files[0])
    }

    return {
      uploadTitle,
      startDate,
      endDate,
      dialogKey,
      showAddDialog,
      postsData,
      enteredLocation,
      searchPerson,
      searchedPeople,
      nameClicked,
      getPeople,
      getAllPosts,
      getPosts,
      openDialog,
      uploadImage,
      disableEndDate,
      disableStartDate
    }
  }
});
</script>

<style scoped>
.action-container {
  display: flex;
  justify-content: center;
}

.name-options {
  position: absolute;
  right: 100px;
  background-color: white;
  border-radius: 0 0 8px 8px;
  z-index: 2;
}

.name-options>ul {
  margin: 0;
  padding: 0;
}

.name-options>ul>li {
  list-style: none;
  margin: .3em 0;
  cursor: pointer;
  padding: .4em .7em;
}

.name-options>ul>li:hover {
  background-color: rgb(250, 249, 249);
}

.input-container {
  display: flex;
  position: relative;
}

.home {
  height: 100%;
}

.search-location {
  border: 0;
  border-bottom: 1px solid rgb(136, 136, 136);
}

.all-btn {
  font-size: 1.2em;
  text-align: center;
  cursor: pointer;
}

.all-btn:hover {
  background-color: rgb(249, 246, 246);
}

.search-input {
  border: 0;
  border-bottom: 1px solid rgb(90, 90, 90);
  padding: .3em .6em;
  font-size: 1.2em;
  width: 100%;
  margin: .2em 0;
}

.home {
  background-color: rgb(228, 234, 240);
  min-height: 100vh;
}

.action-block {
  position: relative;
  margin-top: 1em;
  border-radius: 10px;
  background-color: white;
  padding: 1em;
  width: 650px;
}

.filter-block {
  display: flex;
  margin: .5em 0;
}

.filter-block>span {
  flex-grow: 1;
  width: 100%;
}

.control-card {
  display: flex;
  justify-content: center;
}

.wrapper {
  width: 70%;
}

.upload-file {
  background-color: white;
  cursor: pointer;
  font-size: 1.2em;
  margin: .5em 0;
  padding: .3em;
  border-radius: 10px;
}

.upload-file:hover {
  background-color: rgb(251, 251, 251);
}
</style>
