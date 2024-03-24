<script setup>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faGithub } from "@fortawesome/free-brands-svg-icons";
import { faLink } from "@fortawesome/free-solid-svg-icons";
</script>

<template>
  <header
    id="header"
    class="px-[5%] h-20 text-white bg-blue-500 flex flex-row space-x-12 text-center items-center"
  >
    <img alt="logo" class="h-12 w-12" src="/vite.svg" />
    <span class="text-2xl">Alibaba Cluster Trace Program</span>
    <ul class="text-xl text-white space-x-8">
      <router-link to="/">Home</router-link>
      <router-link to="/dashboard">Dashboard</router-link>
      <router-link to="/table">Table</router-link>
      <router-link to="/trace">Trace</router-link>
      <router-link to="/about">About</router-link>
    </ul>
    <div class="flex-grow"></div>
    <a href="https://github.com/alibaba/clusterdata">
      <font-awesome-icon :icon="faLink" class="h-8 w-8" />
    </a>
    <a href="https://github.com/">
      <font-awesome-icon :icon="faGithub" class="h-8 w-8" />
    </a>
  </header>
</template>

<style scoped></style>
