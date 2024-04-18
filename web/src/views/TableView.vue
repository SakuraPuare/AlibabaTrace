<script setup>
import Tree from "../components/tools/FileListTool.vue";
import http from "../utils/http.js";
import { onMounted, onUnmounted, ref } from "vue";
import { TableV2SortOrder } from "element-plus";
import { getColumnDetails, getHeightWithoutHeader } from "../utils/utils.js";

const TreeData = ref([]);
const selectedItem = ref({});
const getTreeData = () => {
  http.get("/database/list").then((res) => {
    // clear data
    TreeData.value = [];
    let data = res.data;
    data.forEach((item) => {
      TreeData.value.push({
        id: item,
        label: item,
      });
    });
  });
};
const TablePage = ref(1);
const TableData = ref([]);
// const TableDataPage = ref({})
const TableColumns = ref([]);
const getTableData = (name, page = 1) => {
  http
    .get("/database/" + name, {
      params: {
        page: page,
      },
    })
    .then((res) => {
      let data = res.data;
      // console.log(data);
      data.forEach((item) => {
        TableData.value.push(item);
      });
    });
};

const getMoreTableData = () => {
  getTableData(selectedItem.value.id, TablePage.value++);
};

const onSelected = (data) => {
  // console.log(data);
  if (selectedItem.value.id !== data.id) {
    TableColumns.value = [];
    TableData.value = [];
    TablePage.value = 1;
  }

  selectedItem.value = data;
  TableColumns.value = getColumnDetails(data.label);
  getTableData(data.id);
};

const sortState = ref({
  key: TableColumns.value[0]?.key || "",
  order: TableV2SortOrder.ASC,
});
const onSort = (sortBy) => {
  if (sortBy.order === TableV2SortOrder.ASC) {
    // sort by key
    TableData.value = TableData.value.sort((a, b) => {
      return a[sortBy.key].localeCompare(b[sortBy.key]);
    });
  } else {
    TableData.value = TableData.value.sort((a, b) => {
      return b[sortBy.key].localeCompare(a[sortBy.key]);
    });
  }
  sortState.value = sortBy;
};

const ScrollbarHeight = ref(0);
const updateHeight = () => {
  ScrollbarHeight.value = getHeightWithoutHeader();
};

onMounted(() => {
  getTreeData();

  updateHeight();
  addEventListener("resize", updateHeight);
});

onUnmounted(() => {
  removeEventListener("resize", updateHeight);
});
</script>

<template>
  <div class="flex w-full h-full">
    <div
      class="flex flex-col justify-center items-center w-[25%] h-full"
      style="background: #fafafa"
    >
      <Tree
        :allow-multiple="false"
        :data="TreeData"
        :height="ScrollbarHeight"
        :title="'Database List'"
        @select="onSelected"
      />
    </div>
    <div class="flex flex-col max-h-full mx-32 w-full pt-8">
      <!--      {{ selectedItem }}-->
      <span v-if="selectedItem?.label" class="text-2xl"
        >Current Selected:
        <span class="text-xl px-4 my-auto">{{ selectedItem.label }}</span>
      </span>
      <span v-else class="text-2xl"> Not Selected</span>
      <!--      {{ TableData }}-->
      <div class="w-full h-full">
        <el-auto-resizer>
          <template #default="{ height, width }">
            <el-table-v2
              :columns="TableColumns"
              :data="TableData"
              :default-checked-keys="[0]"
              :default-expanded-keys="[1]"
              :fixed="true"
              :height="height"
              :sort-by="sortState"
              :width="width"
              stimated-row-height
              @end-reached="getMoreTableData"
              @column-sort="onSort"
            />
          </template>
        </el-auto-resizer>
      </div>
    </div>
  </div>
  <!--  <ToTop />-->
</template>

<style scoped></style>
