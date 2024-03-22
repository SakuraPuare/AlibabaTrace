<script setup>
import {defineProps, onMounted, onUnmounted, ref} from "vue";
import {getHeightWithoutHeader} from "../../../utils/utils.js";


const updateHeight = () => {
  ScrollbarHeight.value = getHeightWithoutHeader();
};
const Treedata = defineProps({
  data: {
    type: Array,
    default: () => []
  },
})
const ScrollbarHeight = ref(0)

onMounted(() => {
  updateHeight();

  window.addEventListener('resize', updateHeight);
})

onUnmounted(() => {
  window.removeEventListener('resize', updateHeight);
})

</script>

<template>
  <el-scrollbar :height="ScrollbarHeight - 32 + 'px'" class="max-w-[20%] w-full mx-2 my-4" style="background: #fafafa;">
    <el-tree
        :data="Treedata.data"
        accordion
        class="w-full h-fit"
        node-key="id"
        show-checkbox
        style="background: #fafafa;"
    >
      <template #default="{ node, data }">
        <span class="text-base text-black w-full">{{ node.label }}</span>
      </template>
    </el-tree>
  </el-scrollbar>
</template>

<style scoped>

</style>
