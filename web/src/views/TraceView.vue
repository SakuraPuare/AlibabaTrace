<script setup>
import Tree from "../components/tools/TreeTool.vue";
import { onMounted, ref } from "vue";
import http from "../utils/http.js";

const TreeData = ref([]);
const selectedItem = ref({});
const getTreeData = () => {
  http
    .get("/trace/tree")
    .then((res) => {
      // clear data
      TreeData.value = [];

      let data = res.data.data;
      for (let key in data) {
        let children = [];
        for (let file in data[key].files) {
          children.push({
            id: file,
            path: [data[key].name, data[key].files[file]],
            label: data[key].files[file],
            children: [],
          });
        }
        TreeData.value.push({
          id: key,
          path: [data[key].name],
          label: data[key].name,
          children: children,
          disabled: true,
        });
      }
      // sort
      TreeData.value.sort((a, b) => {
        return b.label.localeCompare(a.label, "zh");
      });
      for (let key in TreeData.value) {
        TreeData.value[key].children.sort((a, b) => {
          return a.label.localeCompare(b.label);
        });
      }
    })
    .catch((err) => {
      console.log(err);
    });
};
const onSelected = (data) => {
  console.log(data);
};

onMounted(() => {
  getTreeData();
});
</script>

<template>
  <div class="flex w-full h-full">
    <div
      class="flex flex-col justify-center items-center w-full max-w-[20%] h-full"
      style="background: #fafafa"
    >
      <Tree :data="TreeData" @select="onSelected" />
    </div>
    <div class="flex flex-col max-h-full mx-32 w-full pt-16">
      <div class="w-full h-full"></div>
    </div>
  </div>
</template>

<style scoped></style>
