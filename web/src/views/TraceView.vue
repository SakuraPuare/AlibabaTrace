<script setup>
import Tree from "../components/tools/FileListTool.vue";
import { onMounted, onUnmounted, ref } from "vue";
import http from "../utils/http.js";
import { use } from "echarts/core";
import { GraphChart } from "echarts/charts";
import { TitleComponent, TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import VChart from "vue-echarts";
import { getHeightWithoutHeader } from "../utils/utils.js";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faAdd,
  faCheck,
  faRemove,
  faRotate,
  faShuffle,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";

use([TitleComponent, TooltipComponent, GraphChart, CanvasRenderer]);

const TreeRef = ref(null);
const TreeData = ref([]);
const JobData = ref([]);
const selectedTreeItem = ref({});
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
const onTreeSelected = (data) => {
  // console.log("selected", data);
  if (selectedTreeItem.value.id !== data.id) {
    // TableColumns.value = [];
    // TableData.value = [];
    TablePage.value = 1;
    JobData.value = [];
    TableSet.value = {};
  }

  selectedTreeItem.value = data;
  // TableColumns.value = getColumnDetails(data.path);
  getTableData(data.id, TablePage.value++);
};
const TablePage = ref(1);
// const TableData = ref([]);
const TableSet = ref({});
const getTableData = (name, page = 1) => {
  http
    .get("/database/" + name, {
      params: {
        page: page,
      },
    })
    .then((res) => {
      let data = res.data;
      // preprocess data
      data.forEach((row) => {
        if (!row.job_name) return;
        if (!TableSet.value[row.job_name]) TableSet.value[row.job_name] = [];
        TableSet.value[row.job_name].push(row);
      });

      for (let key in TableSet.value) {
        JobData.value.push({
          id: key,
          label: key,
        });
      }
    });
};
const onJobSelected = (item) => {
  // console.log(item);

  echartsNodes.value = [];
  echartsEdges.value = [];

  item.forEach((job_name) => {
    const jobs = TableSet.value[job_name.id];
    // console.log(jobs);
    jobs?.forEach((job) => {
      // console.log(job);
      let taskName = job.task_name;
      if (taskName.startsWith("task_")) {
        const node = {
          name: taskName,
          x: 0,
          y: 0,
          attributes: job,
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
          name: job_name.id + "_" + taskName,
          x: 0,
          y: 0,
          attributes: job,
        };
        if (!echartsNodes.value.find((n) => n.name === node.name))
          echartsNodes.value.push(node);
      } else {
        for (let i = 1; i <= split.length; i++) {
          const node = {
            name: job_name.id + "_" + split[i - 1],
            x: 0,
            y: 0,
            attributes: job,
          };
          if (!echartsNodes.value.find((n) => n.name === node.name))
            echartsNodes.value.push(node);

          const edge = {
            source: job_name.id + "_" + split[i - 1],
            target: job_name.id + "_" + split[i],
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
  });
  // console.log(echartsNodes.value, echartsEdges.value);
};
const echartsNodes = ref([]);
const echartsEdges = ref([]);
const echartsOption = ref({
  title: {
    text: "Visualize DAG",
  },
  tooltip: {
    formatter: (params) => {
      let str = "";
      // for key value pair
      for (let key in params.data.attributes) {
        str += key + ": " + params.data.attributes[key] + "<br>";
      }
      return str;
    },
  },
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
const echartsHeight = ref(630);

const getEchartsHeight = () => {
  echartsHeight.value = getHeightWithoutHeader() * 0.8;
};

const ScrollbarHeight = ref(0);
const updateHeight = () => {
  ScrollbarHeight.value = getHeightWithoutHeader() - 64 + 8 - 1;
};

const setCheckedNodes = (nodes) => {
  TreeRef.value?.setCheckedNodes(nodes);
  // console.log(TreeRef.value);
};

const loadMore = () => {
  if (selectedTreeItem.value.id === undefined) return;
  getTableData(selectedTreeItem.value.id, TablePage.value++);
};

const selectAll = () => {
  if (JobData.value.length === 0) return;
  setCheckedNodes(JobData.value);
};

const selectNone = () => {
  // console.log("select none");
  if (JobData.value.length === 0) return;
  setCheckedNodes([]);
};

const selectRandom = () => {
  // console.log("select random");
  if (JobData.value.length === 0) return;
  let random = Math.floor(Math.random() * JobData.value.length);
  setCheckedNodes([JobData.value[random]]);
};

const addNode = () => {
  echartsNodes.value.push({
    name: "Node_" + echartsNodes.value.length,
    x: 0,
    y: 0,
  });
};

const removeNode = () => {
  if (echartsNodes.value.length === 0) return;

  let random = Math.floor(Math.random() * echartsNodes.value.length);
  let node = echartsNodes.value[random];
  // remove edges
  echartsEdges.value = echartsEdges.value.filter(
    (edge) => edge.source !== node.name && edge.target !== node.name,
  );

  echartsNodes.value.splice(random, 1);
};

const addEdge = () => {
  let random = Math.floor(Math.random() * echartsNodes.value.length);
  let source = echartsNodes.value[random].name;
  random = Math.floor(Math.random() * echartsNodes.value.length);
  let target = echartsNodes.value[random].name;
  echartsEdges.value.push({
    source: source,
    target: target,
  });
};

const removeEdge = () => {
  if (echartsEdges.value.length === 0) return;

  let random = Math.floor(Math.random() * echartsEdges.value.length);
  echartsEdges.value.splice(random, 1);
};

const shuffle = () => {
  if (echartsNodes.value.length === 0) return;
  // 随机连接各个节点
  echartsEdges.value = [];
  for (let i = 0; i < echartsNodes.value.length; i++) {
    let source = echartsNodes.value[i].name;
    let target =
      echartsNodes.value[Math.floor(Math.random() * echartsNodes.value.length)]
        .name;
    echartsEdges.value.push({
      source: source,
      target: target,
    });
  }
};

onMounted(() => {
  getTreeData();

  updateHeight();
  getEchartsHeight();
  addEventListener("resize", getEchartsHeight);
  addEventListener("resize", updateHeight);
});

onUnmounted(() => {
  removeEventListener("resize", updateHeight);
  removeEventListener("resize", getEchartsHeight);
});
</script>

<template>
  <div class="flex w-full h-full">
    <div
      class="flex flex-col justify-center items-center w-full max-w-[20%] border h-full"
      style="background: #fafafa"
    >
      <Tree
        :data="TreeData"
        :height="ScrollbarHeight * 0.4"
        :title="'File List'"
        @select="onTreeSelected"
      />
      <Tree
        ref="TreeRef"
        :allow-multi-select="true"
        :data="JobData"
        :height="ScrollbarHeight * 0.6"
        :title="'Job List'"
        @select="onJobSelected"
      />

      <div
        class="flex place-content-center items-center h-16 w-full text-white space-x-2"
      >
        <button
          class="flex place-content-center items-center bg-green-500 hover:bg-green-600 active:bg-green-700 h-fit p-2 rounded-3xl space-x-1"
          @click="loadMore"
        >
          <font-awesome-icon :icon="faRotate" class="h-4 w-4" />
          <span>加载</span>
        </button>
        <button
          class="flex place-content-center items-center bg-blue-500 hover:bg-blue-600 active:bg-blue-700 h-fit p-2 rounded-3xl space-x-1"
          @click="selectAll"
        >
          <font-awesome-icon :icon="faCheck" class="h-4 w-4" />
          <span>全选</span>
        </button>
        <button
          class="flex place-content-center items-center bg-red-500 hover:bg-red-600 active:bg-red-700 h-fit p-2 rounded-3xl space-x-1"
          @click="selectNone"
        >
          <font-awesome-icon :icon="faXmark" class="h-4 w-4" />
          <span>全不选</span>
        </button>
        <button
          class="flex place-content-center items-center bg-yellow-500 hover:bg-yellow-600 active:bg-yellow-700 h-fit p-2 rounded-3xl space-x-1"
          @click="selectRandom"
        >
          <font-awesome-icon :icon="faShuffle" class="h-4 w-4" />
          <span>随机</span>
        </button>
      </div>
    </div>
    <!--    v-if="selectedTreeItem?.label"-->
    <div class="flex flex-col max-h-full mx-32 w-full py-4 space-y-4">
      <!--      {{ JobData }}-->
      <!--      {{ selectedTreeItem }}-->
      <div id="echarts" class="h-full w-full border-2 rounded-2xl">
        <v-chart
          :option="echartsOption"
          :style="'height: ' + echartsHeight + 'px'"
        />
      </div>
      <div
        class="flex place-content-center items-center space-x-6 w-full h-16 text-white"
      >
        <button
          class="h-fit min-w-24 p-2 bg-green-500 rounded-2xl border hover:bg-green-600 active:bg-green-700"
          @click="addNode"
        >
          <font-awesome-icon :icon="faAdd" class="h-4 w-4" />
          <span>添加节点</span>
        </button>
        <button
          class="h-fit min-w-24 p-2 bg-red-500 rounded-2xl border hover:bg-red-600 active:bg-red-700"
          @click="removeNode"
        >
          <font-awesome-icon :icon="faRemove" class="h-4 w-4" />
          <span>删除节点</span>
        </button>
        <button
          class="h-fit min-w-24 p-2 bg-green-500 rounded-2xl border hover:bg-green-600 active:bg-green-700"
          @click="addEdge"
        >
          <font-awesome-icon :icon="faAdd" class="h-4 w-4" />
          <span>添加边</span>
        </button>
        <button
          class="h-fit min-w-24 p-2 bg-red-500 rounded-2xl border hover:bg-red-600 active:bg-red-700"
          @click="removeEdge"
        >
          <font-awesome-icon :icon="faRemove" class="h-4 w-4" />
          <span>删除边</span>
        </button>
        <button
          class="h-fit min-w-24 p-2 bg-yellow-500 rounded-2xl border hover:bg-yellow-600 active:bg-yellow-700"
          @click="shuffle"
        >
          <font-awesome-icon :icon="faShuffle" class="h-4 w-4" />
          <span>随机排列</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
