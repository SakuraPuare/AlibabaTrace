<script setup>
import Tree from "../components/tools/TreeTool.vue";
import { onMounted, onUnmounted, ref } from "vue";
import http from "../utils/http.js";
import { getDataSchema } from "../utils/schema.js";
import { use } from "echarts/core";
import { GraphChart } from "echarts/charts";
import { TitleComponent, TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";

use([TitleComponent, TooltipComponent, GraphChart, CanvasRenderer]);

const TreeData = ref([]);
const selectedTreeItem = ref({});
const getTreeData = () => {
  http
    .get("/file/trace")
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

  if (selectedTreeItem.value.id !== data.id) {
    // TableColumns.value = [];
    TableData.value = [];
    TablePage.value = 1;
  }

  selectedTreeItem.value = data;
  if (data.path?.length > 0) {
    // TableColumns.value = getColumnDetails(data.path);
    getTableData(data.id, TablePage.value++);
  } else {
    // TableColumns.value = [];
    TableData.value = [];
    TablePage.value = 1;
  }
};
const TablePage = ref(1);
const TableData = ref([]);
const TableSet = ref({});
const TraceOptions = ref([]);
const selectedTraceItem = ref();
const getTableData = (name, page = 1) => {
  http
    .get("/file/" + name, {
      params: {
        page: page,
      },
    })
    .then((res) => {
      // TableData.value = [];
      const data = res.data.data;
      const schema = getDataSchema(selectedTreeItem.value.path);
      let index = 0;
      for (; index < schema.length; index++)
        if (schema[index][0] === "job_name") break;

      TableData.value = data;

      for (let i = 0; i < data.length; i++) {
        let row = data[i].split(",");
        if (row?.length === 0) break;
        if (!TableSet.value[row[index]]) TableSet.value[row[index]] = [];
        TableSet.value[row[index]].push(row);
      }

      for (let key in TableSet.value) {
        TraceOptions.value.push({
          value: key,
          label: key,
        });
      }
    });
};
const onChange = () => {
  console.log("change");
  // console.log(selectedTraceItem.value);

  echartsNodes.value = [];
  echartsEdges.value = [];

  const schema = getDataSchema(selectedTreeItem.value.path);
  let taskNameIndex = 0;
  for (; taskNameIndex < schema.length; taskNameIndex++)
    if (schema[taskNameIndex][0] === "task_name") break;

  // selectedTraceItem.value = Object.keys(TableSet.value).shu.slice(0, 00);
  // shuffle
  let keys = Object.keys(TableSet.value);
  keys.sort(() => Math.random() - 0.5);
  selectedTraceItem.value = keys.slice(0, 100);

  for (const job in selectedTraceItem.value) {
    const jobName = selectedTraceItem.value[job];
    TableSet.value[jobName].forEach((row) => {
      let taskName = row[taskNameIndex];

      if (taskName.startsWith("task_")) {
        const node = {
          name: taskName,
          x: 0,
          y: 0,
        };
        if (!echartsNodes.value.find((n) => n.name === node.name))
          echartsNodes.value.push(node);
        return;
      }

      // remove the first letter
      taskName = taskName.slice(1);
      const split = taskName.split("_");
      if (split.length === 1) {
        const node = {
          name: jobName + "_" + taskName,
          x: 0,
          y: 0,
        };
        if (!echartsNodes.value.find((n) => n.name === node.name))
          echartsNodes.value.push(node);
      } else {
        // console.log(split);
        for (let i = 1; i <= split.length; i++) {
          const node = {
            name: jobName + "_" + split[i - 1],
            x: 0,
            y: 0,
          };
          if (!echartsNodes.value.find((n) => n.name === node.name))
            echartsNodes.value.push(node);

          const edge = {
            source: jobName + "_" + split[i - 1],
            target: jobName + "_" + split[i],
          };
          if (
            !echartsEdges.value.find(
              (e) => e.source === edge.source && e.target === edge.target,
            )
          )
            echartsEdges.value.push(edge);
        }
      }
    });
  }

  // console.log(echartsNodes.value, echartsEdges.value);
};
const echartsNodes = ref([]);
const echartsEdges = ref([]);
const echartsOption = ref({
  title: {
    text: "Basic Graph",
  },
  tooltip: {},
  animationDurationUpdate: 1500,
  animationEasingUpdate: "quinticInOut",
  series: [
    {
      type: "graph",
      layout: "force",
      force: {
        // initLayout: 'circular'
        // gravity: 10,
        repulsion: 10,
        edgeLength: 1,
      },
      symbolSize: 40,
      roam: true,
      label: {
        show: true,
      },
      edgeSymbol: ["circle", "arrow"],
      edgeSymbolSize: [8, 8],
      edgeLabel: {
        fontSize: 15,
      },
      data: echartsNodes,
      links: echartsEdges,
      lineStyle: {
        opacity: 0.8,
        width: 2,
        curveness: 0,
      },
    },
  ],
});

const echartsHeight = ref(600);

const getEchartsHeight = () => {
  const echarts = document.getElementById("echarts");
  echartsHeight.value = echarts.innerHeight - 64;
  console.log(echartsHeight.value);
};

onMounted(() => {
  getTreeData();

  getEchartsHeight();
  addEventListener("resize", getEchartsHeight);
});

onUnmounted(() => {
  removeEventListener("resize", getEchartsHeight);
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
    <!--    v-if="selectedTreeItem?.label"-->
    <div class="flex flex-col max-h-full mx-32 w-full py-4 space-y-4">
      <el-select-v2
        v-model="selectedTraceItem"
        :options="TraceOptions"
        clearable
        multiple
        placeholder="Select"
        size="large"
        @change="onChange"
      />

      <div id="echarts" class="h-full w-full border-2 rounded-2xl">
        <v-chart
          :class="'h-[' + echartsHeight + 'px]'"
          :option="echartsOption"
        />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
