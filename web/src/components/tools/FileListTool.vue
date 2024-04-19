<script setup>
import { reactive, ref } from "vue";

const getCurrentSelected = () => {
  return treeRef.value?.getCheckedNodes();
};
const setCheckedNodes = (nodes) => {
  treeRef.value?.setCheckedNodes(nodes);
  // console.log(treeRef.value);
  if (treeData.allowMultiSelect) {
    currSelected.value = nodes;
    emits("select", currSelected.value);
  } else {
    currSelected.value = nodes;
    emits("select", currSelected.value);
  }
};

const onClick = (data) => {
  // if selected
  let selected = getCurrentSelected();
  // console.log(selected);
  if (selected?.length === 0) {
    setCheckedNodes([{}]);
    return;
  }
  if (treeData.allowMultiSelect) {
    setCheckedNodes(selected);
  } else setCheckedNodes([data]);
};

const treeData = defineProps({
  title: {
    type: String,
    default: "",
  },
  height: {
    type: Number,
    default: 0,
  },
  data: {
    type: Array,
    default: () => [],
  },
  allowMultiSelect: {
    type: Boolean,
    default: false,
  },
});
const treeRef = ref(null);
const currSelected = reactive({});

const emits = defineEmits(["select"]);

defineExpose({
  setCheckedNodes,
  getCurrentSelected,
});
</script>

<template>
  <span class="text-2xl text-black text-center mt-2">
    {{ treeData.title }}
  </span>
  <el-scrollbar
    :height="treeData.height - 32 - 32 + 4 + 'px'"
    class="w-full mt-4"
  >
    <el-tree
      ref="treeRef"
      :data="treeData.data"
      accordion
      check-on-click-node
      class="w-full h-fit"
      highlight-current
      node-key="id"
      show-checkbox
      style="background: #fafafa"
      @check="onClick"
    >
      <template #default="{ node }">
        <span class="text-base text-black w-full">{{ node.label }}</span>
      </template>
    </el-tree>
  </el-scrollbar>
</template>

<style scoped></style>
