<script setup>
import Header from "../components/Header.vue";
import ToTop from "../components/tools/ToTop.vue";
import Tree from "../components/tools/Tree.vue";
import http from "../../utils/http.js";
import {ref, onMounted} from "vue";

const getTree = () => {
  http.get('/table/tree').then(
      res => {
        let data = res.data.data
        for (let key in data) {
          let children = [];
          for (let file in data[key].files) {
            children.push({
              label: data[key].files[file],
              children: [],
            })
          }
          TreeData.value.push({
            label: data[key].name,
            children: children,
            disabled: true
          })
        }
        // sort
        TreeData.value.sort((a, b) => {
          return b.label.localeCompare(a.label, 'zh')
        })
        for (let key in TreeData.value) {
          TreeData.value[key].children.sort((a, b) => {
            return a.label.localeCompare(b.label)
          })
        }
      }
  ).catch(
      err => {
        console.log(err)
      }
  )
}
const TreeData = ref([]);

onMounted(() => {
  getTree()
})
</script>

<template>
  <Header class="flex-none"/>
  <div class="flex flex-col">
    <div class="flex flex-row h-full" style="background: #fafafa;">
      <Tree :data="TreeData"/>
      <div class="flex-grow"></div>
    </div>
  </div>
  <ToTop/>
</template>

<style scoped>

</style>
