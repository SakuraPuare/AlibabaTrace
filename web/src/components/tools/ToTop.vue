<script setup>

import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {faAngleUp} from "@fortawesome/free-solid-svg-icons";
import {onMounted, onUnmounted, ref} from "vue";

function toTop() {
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
}

const showIcon = ref(false);

const checkScroll = () => {
  showIcon.value = window.scrollY > 200; // change 200 to the distance you want
};

onMounted(() => {
  window.addEventListener('scroll', checkScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', checkScroll);
});

</script>

<template>
  <!--  if rotate -->
  <el-affix v-if="showIcon">
    <div class="to-top fixed bottom-12 right-12 h-12 w-12 rounded-full bg-blue-500 flex items-center justify-center"
         @click="toTop">
      <FontAwesomeIcon :icon="faAngleUp" class="h-6 w-6 text-white"/>
    </div>
  </el-affix>
</template>

<style scoped>

</style>
