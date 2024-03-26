<script setup>
import Tree from "../components/tools/TreeTool.vue";
import http from "../utils/http.js";
import { onMounted, ref } from "vue";
import { getColumnDetails } from "../utils/utils.js";
import { TableV2SortOrder } from "element-plus";

const TreeData = ref([]);
const selectedItem = ref({});
const getTreeData = () => {
  http
    .get("/file/tree")
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
const TablePage = ref(1);
const TableData = ref([]);
// const TableDataPage = ref({})
const TableColumns = ref([]);
const getTableData = (name, page = 1) => {
  http
    .get("/file/" + name, {
      params: {
        page: page,
      },
    })
    .then((res) => {
      TableData.value = [];
      let data = res.data.data;

      if (selectedItem.value.path[0].startsWith("microservice"))
        // remove the first line
        data.shift();
      // console.log(data);
      for (let i = 0; i < data.length; i++) {
        let row = data[i].split(",");
        if (row?.length === 0) break;
        let obj = {};
        // remove last empty column
        for (let j = 0; j < row.length; j++) {
          const k = TableColumns.value[j]?.key;
          if (!k) break;
          obj[k] = row[j];
        }
        TableData.value.push(obj);
      }
    });
};
const getMoreTableData = () => {
  if (TableData.value.length === 0) {
    return;
  }

  http
    .get("/file/" + selectedItem.value.id, {
      params: {
        page: TablePage.value++,
      },
    })
    .then((res) => {
      let data = res.data.data;

      if (selectedItem.value.path[0].startsWith("microservices"))
        // remove the first line
        data.shift();

      for (let i = 0; i < data.length; i++) {
        let row = data[i].split(",");
        let obj = {};

        for (let j = 0; j < row.length; j++) {
          const k = TableColumns.value[j]?.key;
          if (!k) break;
          obj[k] = row[j];
        }
        TableData.value.push(obj);
      }
    });
};
const onSelected = (data) => {
  // console.log(data)
  if (selectedItem.value.id !== data.id) {
    TableColumns.value = [];
    TableData.value = [];
    TablePage.value = 1;
  }

  selectedItem.value = data;
  if (data.path?.length > 0) {
    TableColumns.value = getColumnDetails(data.path);
    getTableData(data.id, TablePage.value++);
  } else {
    TableColumns.value = [];
    TableData.value = [];
    TablePage.value = 1;
  }
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

onMounted(() => {
  getTreeData();
});
</script>

<template>
  <div class="flex w-full h-full">
    <div
      class="flex flex-col justify-center items-center w-[25%] h-full"
      style="background: #fafafa"
    >
      <Tree :data="TreeData" @select="onSelected" />
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
