<script setup>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faGithub } from "@fortawesome/free-brands-svg-icons";
import { faLink } from "@fortawesome/free-solid-svg-icons";
</script>

<template>
  <header
    id="header"
    class="px-[5%] h-16 text-white bg-blue-500 flex flex-row space-x-8 text-center items-center justify-center"
  >
    <img alt="logo" class="h-8 w-8" src="/vite.svg" />
    <router-link to="/">
      <span class="text-xl font-bold">基于Python的阿里数据集分析及可视化系统</span>
    </router-link>
    <ul class="text-base text-white space-x-8">
      <router-link to="/dashboard">数据可视化分析</router-link>
      <router-link to="/table">数据表可视化分析</router-link>
      <router-link to="/trace">有向图可视化分析</router-link>
      <router-link to="/analyse">算法应用可视化分析</router-link>
      <!-- <router-link to="/about">About</router-link> -->
    </ul>
    <div class="flex-grow"></div>
    <div class="flex flex-row items-center justify-center space-x-8">
      <span>
        <a href="https://github.com/alibaba/clusterdata">
          <font-awesome-icon :icon="faLink" class="h-6 w-6" />
        </a>
      </span>
      <span>
        <a href="https://github.com/">
          <div>
            <font-awesome-icon :icon="faGithub" class="h-6 w-6" />
          </div>
        </a>
      </span>
    </div>
  </header>
</template>

<style scoped></style>
