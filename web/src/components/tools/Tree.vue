<script setup>
import {onMounted, onUnmounted, reactive, ref} from "vue";
import {getHeightWithoutHeader} from "../../../utils/utils.js";


const updateHeight = () => {
  ScrollbarHeight.value = getHeightWithoutHeader();
};

const getCurrentSelected = () => {
  return treeRef.value?.getCheckedNodes()
}
const setCheckedNodes = (nodes) => {
  treeRef.value?.setCheckedNodes(nodes)
  currSelected.value = nodes[0]
  emits('select', currSelected.value)
}

const handleClickOnCheck = (data) => {
  console.log('click on check')

  // if selected
  let selected = getCurrentSelected()
  console.log(selected)
  if (selected?.length === 0) {
    setCheckedNodes([{}])
    return
  }
  setCheckedNodes([data])
}

const handleClickOnNode = (data) => {
  if (data.disabled) {
    return
  }

  // if selected
  let selected = getCurrentSelected()
  if (selected.length > 0 && selected[0].id === data.id) {
    // unselect
    setCheckedNodes([{}])
    return;
  }
  setCheckedNodes([data])
}

const treeData = defineProps({
  data: {
    type: Array,
    default: () => []
  },
})
const treeRef = ref(null)
const currSelected = reactive({})

const ScrollbarHeight = ref(0)

const emits = defineEmits(['select'])

onMounted(() => {
  updateHeight();

  window.addEventListener('resize', updateHeight);
})

onUnmounted(() => {
  window.removeEventListener('resize', updateHeight);
})

</script>

<template>
  <span class="text-2xl text-black text-center my-2"> File Tree </span>
  <el-scrollbar :height="ScrollbarHeight - 32 - 32 - 8 + 'px'" class="w-full mt-4">
    <el-tree
        ref="treeRef"
        :data="treeData.data"
        accordion
        class="w-full h-fit"
        node-key="id"
        show-checkbox
        style="background: #fafafa;"
        @check="handleClickOnCheck"
        @node-click="handleClickOnNode"
    >
      <template #default="{ node, data }">
        <span class="text-base text-black w-full" >{{ node.label }}</span>
      </template>
    </el-tree>
  </el-scrollbar>
</template>

<style scoped>

</style>
