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
  data = data[0];
  if (selectedTreeItem.value.id !== data.id) {
    // TableColumns.value = [];
    // TableData.value = [];
    TablePage.value = 1;
    JobData.value = [];
    TableSet.value = {};

    SelectValue.value = "";
  }

  selectedTreeItem.value = data;
  // TableColumns.value = getColumnDetails(data.path);
  getTableData(data.id, TablePage.value++);
};
const TablePage = ref(1);
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
        for (let i = 1; i < split.length; i++) {
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
};
const EchartsRef = ref(null);
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
        str += `${key}: ${params.data.attributes[key]}<br>`;
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
      symbolSize: 80,
      roam: true,
      label: {
        show: true,
        fontWeight: "bold",
      },
      edgeSymbol: ["circle", "arrow"],
      edgeSymbolSize: [8, 8],
      edgeLabel: {
        fontSize: 20,
      },
      data: echartsNodes,
      links: echartsEdges,
      lineStyle: {
        opacity: 1,
        width: 2,
        curveness: 0,
      },
    },
  ],
  method: "post",
});

const updateEchartsHeight = () => {
  EchartsRef.value?.resize({ width: "auto", height: "auto" });
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
  const name = "Node_" + echartsNodes.value.length;
  echartsNodes.value.push({
    name: name,
    x: 0,
    y: 0,
    attributes: {},
  });

  if (addNodeDirection.value === "in") {
    if (!addNodeIsolated.value) {
      // find add edges that from addNodeValue
      let edges = echartsEdges.value.filter(
        (edge) => edge.target === addNodeValue.value,
      );
      edges.forEach((edge) => {
        edge.target = name;
      });
    }
    echartsEdges.value.push({
      source: name,
      target: addNodeValue.value,
    });
  } else if (addNodeDirection.value === "out") {
    if (!addNodeIsolated.value) {
      // find add edges that to addNodeValue
      let edges = echartsEdges.value.filter(
        (edge) => edge.source === addNodeValue.value,
      );
      edges.forEach((edge) => {
        edge.source = name;
      });
    }
    echartsEdges.value.push({
      source: addNodeValue.value,
      target: name,
    });
  }
  addNodeValue.value = "";
};

const removeNode = () => {
  let node = echartsNodes.value.find((o) => o.name === removeNodeValue.value);
  if (!node) return;
  console.log(node);

  let sourceEdges = echartsEdges.value.filter(
    (edge) => edge.target === node.name,
  );
  let targetEdges = echartsEdges.value.filter(
    (edge) => edge.source === node.name,
  );

  if (
    !removeNodeConnection.value ||
    !(sourceEdges.length === 1 && targetEdges.length === 1)
  ) {
    echartsEdges.value = echartsEdges.value.filter(
      (edge) => !(edge.source === node.name || edge.target === node.name),
    );
  } else {
    sourceEdges[0].target = targetEdges[0].target;
    targetEdges[0].source = sourceEdges[0].source;
  }
  echartsNodes.value = echartsNodes.value.filter((n) => n.name !== node.name);

  removeNodeValue.value = "";
};

const addEdge = () => {
  if (addEdgeFrom.value === addEdgeTo.value) return;

  // if the edge already exists
  if (
    echartsEdges.value.find(
      (edge) =>
        edge.source === addEdgeFrom.value && edge.target === addEdgeTo.value,
    )
  )
    return;

  echartsEdges.value.push({
    source: addEdgeFrom.value,
    target: addEdgeTo.value,
  });
  addEdgeFrom.value = "";
  addEdgeTo.value = "";
};

const removeEdge = () => {
  echartsEdges.value = echartsEdges.value.filter(
    (edge) =>
      !(
        removeEdgeFrom.value.includes(edge.source) &&
        removeEdgeTo.value.includes(edge.target)
      ),
  );
  removeEdgeFrom.value = "";
  removeEdgeTo.value = "";
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

const resetNode = () => {
  let curr = TreeRef.value?.getCurrentSelected();
  if (curr.length === 0) return;
  onJobSelected(curr);
};

onMounted(() => {
  getTreeData();
  updateHeight();
  updateEchartsHeight();
  addEventListener("resize", updateEchartsHeight);
  addEventListener("resize", updateHeight);
});

onUnmounted(() => {
  removeEventListener("resize", updateHeight);
  removeEventListener("resize", updateEchartsHeight);
});

const SelectValue = ref("");

const onSelectChange = () => {
  if (SelectValue.value === "") {
    DetailData.value = [];
    return;
  }

  let job = echartsNodes.value.find((o) => o.name === SelectValue.value);
  DetailData.value = Object.entries(job.attributes);
  // console.log(DetailData.value);
};

const DetailData = ref([]);

const showAddNodeDialog = ref(false);
const showRemoveNodeDialog = ref(false);
const showAddEdgeDialog = ref(false);
const showRemoveEdgeDialog = ref(false);
const addNodeValue = ref("");
const addNodeDirection = ref("");
const addNodeIsolated = ref(false);
const removeNodeValue = ref("");
const removeNodeConnection = ref(true);
const addEdgeFrom = ref("");
const addEdgeTo = ref("");
const removeEdgeFrom = ref("");
const removeEdgeTo = ref("");

const onEchatsClick = (params) => {
  // console.log(params);
  if (params.dataType === "node") {
    SelectValue.value = params.data.name;
    DetailData.value = Object.entries(params.data.attributes);
  }
};
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
          <span class="sm:invisible md:visible">加载</span>
        </button>
        <button
          class="flex place-content-center items-center bg-blue-500 hover:bg-blue-600 active:bg-blue-700 h-fit p-2 rounded-3xl space-x-1"
          @click="selectAll"
        >
          <font-awesome-icon :icon="faCheck" class="h-4 w-4" />
          <span class="sm:invisible md:visible">全选</span>
        </button>
        <button
          class="flex place-content-center items-center bg-red-500 hover:bg-red-600 active:bg-red-700 h-fit p-2 rounded-3xl space-x-1"
          @click="selectNone"
        >
          <font-awesome-icon :icon="faXmark" class="h-4 w-4" />
          <span class="sm:invisible md:visible">全不选</span>
        </button>
        <button
          class="flex place-content-center items-center bg-yellow-500 hover:bg-yellow-600 active:bg-yellow-700 h-fit p-2 rounded-3xl space-x-1"
          @click="selectRandom"
        >
          <font-awesome-icon :icon="faShuffle" class="h-4 w-4" />
          <span class="sm:invisible md:visible">随机</span>
        </button>
      </div>
    </div>
    <!--    v-if="selectedTreeItem?.label"-->
    <div class="flex flex-col max-h-full mx-16 w-full py-4 space-y-4">
      <!--      {{ JobData }}-->
      <!--      {{ selectedTreeItem }}-->
      <div id="echarts" class="h-full w-full border-2 rounded-2xl">
        <v-chart
          ref="EchartsRef"
          :option="echartsOption"
          @click="onEchatsClick"
        />
      </div>
      <div
        class="flex place-content-center items-center space-x-6 w-full h-16 text-white"
      >
        <button
          class="h-fit min-w-24 p-2 bg-blue-500 rounded-2xl border hover:bg-blue-600 active:bg-blue-700"
          @click="resetNode"
        >
          <font-awesome-icon :icon="faRotate" class="h-4 w-4" />
          <span class="">重新加载</span>
        </button>
        <button
          class="h-fit min-w-24 p-2 bg-green-500 rounded-2xl border hover:bg-green-600 active:bg-green-700"
          @click="showAddNodeDialog = true"
        >
          <font-awesome-icon :icon="faAdd" class="h-4 w-4" />
          <span class="">添加节点</span>
        </button>
        <button
          class="h-fit min-w-24 p-2 bg-red-500 rounded-2xl border hover:bg-red-600 active:bg-red-700"
          @click="showRemoveNodeDialog = true"
        >
          <font-awesome-icon :icon="faRemove" class="h-4 w-4" />
          <span class="">删除节点</span>
        </button>
        <button
          class="h-fit min-w-24 p-2 bg-green-500 rounded-2xl border hover:bg-green-600 active:bg-green-700"
          @click="showAddEdgeDialog = true"
        >
          <font-awesome-icon :icon="faAdd" class="h-4 w-4" />
          <span class="">添加边</span>
        </button>
        <button
          class="h-fit min-w-24 p-2 bg-red-500 rounded-2xl border hover:bg-red-600 active:bg-red-700"
          @click="showRemoveEdgeDialog = true"
        >
          <font-awesome-icon :icon="faRemove" class="h-4 w-4" />
          <span class="">删除边</span>
        </button>
        <button
          class="h-fit min-w-24 p-2 bg-yellow-500 rounded-2xl border hover:bg-yellow-600 active:bg-yellow-700"
          @click="shuffle"
        >
          <font-awesome-icon :icon="faShuffle" class="h-4 w-4" />
          <span class="">随机排列</span>
        </button>
      </div>
    </div>
    <div
      :style="'height: ' + getHeightWithoutHeader() + 'px'"
      class="flex flex-warp flex-col items-center justify-center place-content-center space-y-4 w-[40%] bg-gray-100 border"
    >
      <el-select
        v-model="SelectValue"
        placeholder="Select"
        size="large"
        style="width: 300px"
        @change="onSelectChange"
      >
        <el-option
          v-for="item in echartsNodes"
          :key="item.name"
          :label="item.name"
          :value="item.name"
        />
      </el-select>

      <div class="bg-white w-[300px] rounded border m-4 text-center">
        <table v-if="SelectValue" class="w-full">
          <tr>
            <th>Key</th>
            <th>Value</th>
          </tr>

          <tr v-for="(i, index) of DetailData" :key="index">
            <td>{{ i[0] }}</td>
            <td>{{ i[1] }}</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
  <div>
    <el-dialog
      v-model="showAddNodeDialog"
      draggable
      title="要添加到哪个节点上？"
    >
      <div
        class="flex flex-col place-content-center justify-center items-center space-y-4"
      >
        <el-select
          v-model="addNodeValue"
          placeholder="Select Node"
          size="large"
          style="width: 500px"
          @change="onSelectChange"
        >
          <el-option
            v-for="item in echartsNodes"
            :key="item.name"
            :label="item.name"
            :value="item.name"
          />
        </el-select>
        <el-select
          v-model="addNodeDirection"
          placeholder="Select Direction"
          size="large"
          style="width: 500px"
        >
          <el-option label="指离节点" value="out" />
          <el-option label="指向节点" value="in" />
        </el-select>
        <el-checkbox v-model="addNodeIsolated">Isolated</el-checkbox>
        <el-button class="w-fit" type="primary" @click="addNode"
          >添加
        </el-button>
      </div>
    </el-dialog>
    <el-dialog
      v-model="showRemoveNodeDialog"
      draggable
      title="要删除哪个节点？"
    >
      <div
        class="flex flex-col place-content-center justify-center items-center space-y-4"
      >
        <el-select
          v-model="removeNodeValue"
          placeholder="Select Node"
          size="large"
          style="width: 500px"
          @change="onSelectChange"
        >
          <el-option
            v-for="item in echartsNodes"
            :key="item.name"
            :label="item.name"
            :value="item.name"
          />
        </el-select>
        <el-checkbox v-model="removeNodeConnection">保持连接</el-checkbox>
        <el-button class="w-fit" type="danger" @click="removeNode"
          >删除
        </el-button>
      </div>
    </el-dialog>
    <el-dialog
      v-model="showAddEdgeDialog"
      draggable
      title="要添加从谁到谁的边？"
    >
      <div
        class="flex flex-col place-content-center justify-center items-center space-y-4"
      >
        <el-select
          v-model="addEdgeFrom"
          placeholder="Select Node"
          size="large"
          style="width: 500px"
          @change="onSelectChange"
        >
          <el-option
            v-for="item in echartsNodes"
            :key="item.name"
            :label="item.name"
            :value="item.name"
          />
        </el-select>
        <el-select
          v-model="addEdgeTo"
          placeholder="Select Node"
          size="large"
          style="width: 500px"
          @change="onSelectChange"
        >
          <el-option
            v-for="item in echartsNodes"
            :key="item.name"
            :label="item.name"
            :value="item.name"
          />
        </el-select>
        <el-button class="w-fit" type="primary" @click="addEdge"
          >添加
        </el-button>
      </div>
    </el-dialog>
    <el-dialog v-model="showRemoveEdgeDialog" draggable title="要删除哪条边？">
      <div
        class="flex flex-col place-content-center justify-center items-center space-y-4"
      >
        <el-select
          v-model="removeEdgeFrom"
          placeholder="Select Node From"
          size="large"
          style="width: 500px"
          @change="onSelectChange"
        >
          <el-option
            v-for="item in echartsNodes"
            :key="item.name"
            :label="item.name"
            :value="item.name"
          />
        </el-select>
        <el-select
          v-model="removeEdgeTo"
          placeholder="Select Node To"
          size="large"
          style="width: 500px"
          @change="onSelectChange"
        >
          <el-option
            v-for="item in echartsNodes"
            :key="item.name"
            :label="item.name"
            :value="item.name"
          />
        </el-select>
        <el-button class="w-fit" type="danger" @click="removeEdge"
          >删除
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped></style>
