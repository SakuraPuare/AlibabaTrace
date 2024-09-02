<script lang="ts" setup>
import Tree from "../components/tools/FileListTool.vue";
import { onMounted, onUnmounted, ref } from "vue";
import http from "../utils/http.js";
import { computed } from "vue";
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

import { use } from "echarts/core";
import { LineChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent,
  GridComponent,
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";

use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent,
  GridComponent,
  LineChart,
  CanvasRenderer,
]);

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

// 16 null
const EchartsRef = ref([
  ref(null),
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
  null,
]);

const updateEchartsHeight = () => {
  // EchartsRef.value?.resize({ width: "auto", height: "auto" });
  for (let i = 0; i < EchartsRef.value.length; i++) {
    EchartsRef.value[i]?.resize({ width: "auto", height: "auto" });
  }
};

const ScrollbarWidth = ref(0);
const ScrollbarHeight = ref(0);
const updateHeight = () => {
  ScrollbarHeight.value = getHeightWithoutHeader() - 64 + 8 - 1;
  ScrollbarWidth.value = document.body.clientWidth - 340;

  chartsHeight.value = ((ScrollbarHeight.value - 128) / 2).toFixed(0);
  chartsWidth.value = ((ScrollbarWidth.value - 128 - 32) / 2).toFixed(0);
};

const setCheckedNodes = (nodes) => {
  TreeRef.value?.setCheckedNodes(nodes);
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

const algorithmList = ["RO", "GO", "DE", "RETO"];
const selectedAlgorithmList = ref(["RO", "GO"]);

const toggle = () => {
  for (let i = 0; i < EchartsRef.value.length; i++) {
    EchartsRef.value[i]?.setOption(
      generateOptions(rawData[Math.floor(i / 4)][i % 4]),
    );
  }
};
const toggleVariable = (variable) => {
  activeName.value = variable;
  toggle();
};

const toggleAlgorithm = (algorithm) => {
  if (selectedAlgorithmList.value.includes(algorithm)) {
    selectedAlgorithmList.value = selectedAlgorithmList.value.filter(
      (item) => item !== algorithm,
    );
  } else {
    selectedAlgorithmList.value.push(algorithm);
  }

  toggle();
};

const generateOptions = (data: {
  title: string;
  legend: string[];
  xAxis: string[];
  series: number[][];
}) => {
  return {
    title: {
      text: data.title,
    },
    tooltip: {
      trigger: "axis",
    },
    legend: {
      data: selectedAlgorithmList.value,
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      boundaryGap: false,
      data: data.xAxis,
    },
    yAxis: {
      type: "value",
    },
    series: data.series.map((item, index) => {
      if (selectedAlgorithmList.value.includes(data.legend[index])) {
        console.log(data.legend[index], item);
        return {
          name: data.legend[index],
          type: "line",
          // stack: "Total",
          data: item,
        };
      }
      return {
        name: data.legend[index],
        type: "line",
        // stack: "Total",
        data: [],
      };
    }),
  };
};
const activeName = ref("first");

const chartsHeight = ref(300);
const chartsWidth = ref(600);

const buttonData = [
  {
    icon: faAdd,
    text: "加载",
    click: loadMore,
    color: "green",
  },
  {
    icon: faCheck,
    text: "全选",
    click: selectAll,
    color: "blue",
  },
  {
    icon: faXmark,
    text: "全不选",
    click: selectNone,
    color: "red",
  },
  {
    icon: faShuffle,
    text: "随机",
    click: selectRandom,
    color: "yellow",
  },
];

const rawData = [
  [
    {
      title: "应用完成时间",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["25", "30", "35", "40"],
      series: [
        [0.408807734, 0.407292937, 0.388917701, 0.3884352],
        [0.312536942, 0.312536942, 0.312536942, 0.312536942],
        [0.355234386, 0.343354255, 0.394375517, 0.342540434],
        [0.237277302, 0.236285645, 0.235168993, 0.236553867],
      ],
      //       RO	GO	DE	RETO
      // 25	0.408807734	0.312536942	0.355234386	0.237277302
      // 30	0.407292937	0.312536942	0.343354255	0.236285645
      // 35	0.388917701	0.312536942	0.394375517	0.235168993
      // 40	0.3884352	0.312536942	0.342540434	0.236553867
    },
    {
      title: "可靠性",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["25", "30", "35", "40"],
      series: [
        [0.5, 0.6, 0.54, 0.54],
        [0.62, 0.62, 0.62, 0.62],
        [0.68, 0.66, 0.66, 0.68],
        [0.9, 0.9, 0.92, 0.92],
      ],
      //       可靠性
      // 	RO	GO	DE	RETO
      // 25	0.5	0.62	0.68	0.9
      // 30	0.6	0.62	0.66	0.9
      // 35	0.54	0.62	0.66	0.92
      // 40	0.54	0.62	0.68	0.92
    },
    {
      title: "带宽资源消耗",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["25", "30", "35", "40"],
      series: [
        [2981, 2817, 2842, 2822],
        [2711, 2695, 2679, 2695],
        [2251, 2209, 2229, 2279],
        [2097, 2180, 2166, 2193],
      ],
      //       带宽资源消耗
      // 	RO	GO	DE	RETO
      // 25	2981	2711	2251	2097
      // 30	2817	2695	2209	2180
      // 35	2842	2679	2229	2166
      // 40	2822	2695	2279	2193
    },
    {
      title: "算法执行时间",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["25", "30", "35", "40"],
      series: [
        [16, 12, 16, 21],
        [20, 12, 18, 30],
        [1278, 1281, 1243, 1166],
        [36, 42, 57, 46],
      ],
      //       RO	GO	DE	RETO
      // 25	16	20	1278	36
      // 30	12	12	1281	42
      // 35	16	18	1243	57
      // 40	21	30	1166	46
    },
  ],
  [
    {
      title: "应用完成时间",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["160", "180", "200", "220"],
      series: [
        [0.367610967, 0.355040588, 0.475896654, 0.364664613],
        [0.362739501, 0.330425145, 0.312536942, 0.296710301],
        [0.354853344, 0.366562468, 0.345778293, 0.357780138],
        [0.252611139, 0.240916771, 0.237277302, 0.228433958],
      ],
      //       应用完成时间
      // 	RO	GO	DE	RETO
      // 160	0.367610967	0.362739501	0.354853344	0.252611139
      // 180	0.355040588	0.330425145	0.366562468	0.240916771
      // 200	0.475896654	0.312536942	0.345778293	0.237277302
      // 220	0.364664613	0.296710301	0.357780138	0.228433958
    },
    {
      title: "可靠性",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["160", "180", "200", "220"],
      series: [
        [0.56, 0.64, 0.54, 0.64],
        [0.54, 0.58, 0.62, 0.64],
        [0.78, 0.72, 0.72, 0.76],
        [0.86, 0.88, 0.9, 0.94],
      ],
      //       可靠性
      // 	RO	GO	DE	RETO
      // 160	0.56	0.54	0.78	0.86
      // 180	0.64	0.58	0.72	0.88
      // 200	0.54	0.62	0.72	0.9
      // 220	0.64	0.64	0.76	0.94
    },
    {
      title: "带宽资源消耗",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["160", "180", "200", "220"],
      series: [
        [2643, 2780, 2837, 3002],
        [2786, 2706, 2711, 2634],
        [2392, 2241, 2253, 2380],
        [2173, 2068, 2097, 2135],
      ],

      // 带宽资源消耗
      // 	RO	GO	DE	RETO
      // 160	2643	2786	2392	2173
      // 180	2780	2706	2241	2068
      // 200	2837	2711	2253	2097
      // 220	3002	2634	2380	2135
    },
    {
      title: "算法执行时间",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["160", "180", "200", "220"],
      series: [
        [21, 17, 35, 13],
        [19, 19, 18, 14],
        [1283, 1276, 1184, 1275],
        [46, 46, 47, 43],
      ],
      // 算法执行时间
      // 	RO	GO	DE	RETO
      // 160	21	19	1283	46
      // 180	17	19	1276	46
      // 200	35	18	1184	47
      // 220	13	14	1275	43
    },
  ],
  [
    {
      title: "应用完成时间",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["20", "30", "40", "50"],
      series: [
        [0.148374831, 0.216105569, 0.316268815, 0.420680987],
        [0.087557457, 0.152836877, 0.220549782, 0.312536942],
        [0.104032107, 0.22997261, 0.288731518, 0.353841621],
        [0.081806942, 0.132586625, 0.180747508, 0.237277302],
      ],
      //       应用完成时间
      // 	RO	GO	DE	RETO
      // 20	0.148374831	0.087557457	0.104032107	0.081806942
      // 30	0.216105569	0.152836877	0.22997261	0.132586625
      // 40	0.316268815	0.220549782	0.288731518	0.180747508
      // 50	0.420680987	0.312536942	0.353841621	0.237277302
    },
    {
      title: "可靠性",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["20", "30", "40", "50"],
      series: [
        [0.55, 0.7, 0.55, 0.5],
        [0.85, 0.766666667, 0.725, 0.62],
        [0.88, 0.8, 0.725, 0.7],
        [0.91, 0.966666667, 0.95, 0.9],
      ],
      // 可靠性
      // 	RO	GO	DE	RETO
      // 20	0.55	0.85	0.88	0.91
      // 30	0.7	0.766666667	0.8	0.966666667
      // 40	0.55	0.725	0.725	0.95
      // 50	0.5	0.62	0.7	0.9
    },
    {
      title: "带宽资源消耗",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["20", "30", "40", "50"],
      series: [
        [1167, 1705, 2345, 2912],
        [982, 1543, 2103, 2711],
        [865, 1246, 1775, 2173],
        [862, 1162, 1670, 2097],
      ],
      // 带宽资源消耗
      // 	RO	GO	DE	RETO
      // 20	1167	982	865	862
      // 30	1705	1543	1246	1162
      // 40	2345	2103	1775	1670
      // 50	2912	2711	2173	2097
    },
    {
      title: "算法执行时间",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["20", "30", "40", "50"],
      series: [
        [10, 17, 17, 28],
        [12, 14, 17, 18],
        [675, 863, 1236, 1432],
        [30, 47, 43, 49],
      ],
      // 算法执行时间
      // 	RO	GO	DE	RETO
      // 20	10	12	675	30
      // 30	17	14	863	47
      // 40	17	17	1236	43
      // 50	28	18	1432	49
    },
  ],
  [
    {
      title: "应用完成时间",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["R1", "R2", "R3", "R4"],
      series: [
        [0.387410635, 0.392944948, 0.423129617, 0.359863624],
        [0.312536942, 0.312536942, 0.312536942, 0.312536942],
        [0.409891051, 0.352099335, 0.369325997, 0.366795246],
        [0.237277302, 0.237277302, 0.237277302, 0.237277302],
      ],
      //       应用完成时间
      // 	RO	GO	DE	RETO
      // R1	0.387410635	0.312536942	0.409891051	0.237277302
      // R2	0.392944948	0.312536942	0.352099335	0.237277302
      // R3	0.423129617	0.312536942	0.369325997	0.237277302
      // R4	0.359863624	0.312536942	0.366795246	0.237277302
    },
    {
      title: "可靠性",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["R1", "R2", "R3", "R4"],
      series: [
        [0.46, 0.48, 0.52, 0.64],
        [0.5, 0.54, 0.58, 0.62],
        [0.54, 0.62, 0.66, 0.7],
        [0.7, 0.76, 0.86, 0.9],
      ],
      // 可靠性
      // 	RO	GO	DE	RETO
      // R1	0.46	0.5	0.54	0.7
      // R2	0.48	0.54	0.62	0.76
      // R3	0.52	0.58	0.66	0.86
      // R4	0.64	0.62	0.7	0.9
    },
    {
      title: "带宽资源消耗",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["R1", "R2", "R3", "R4"],
      series: [
        [2853, 2864, 2964, 3010],
        [2711, 2711, 2711, 2711],
        [2242, 2275, 2301, 2265],
        [2097, 2097, 2097, 2097],
      ],
      // 带宽资源消耗
      // 	RO	GO	DE	RETO
      // R1	2853	2711	2242	2097
      // R2	2864	2711	2275	2097
      // R3	2964	2711	2301	2097
      // R4	3010	2711	2265	2097
    },
    {
      title: "算法执行时间",
      legend: ["RO", "GO", "DE", "RETO"],
      xAxis: ["R1", "R2", "R3", "R4"],
      series: [
        [17, 20, 18, 13],
        [34, 20, 17, 46],
        [1291, 1478, 1261, 1300],
        [45, 54, 46, 48],
      ],
      // 算法执行时间
      // 	RO	GO	DE	RETO
      // R1	17	34	1291	45
      // R2	20	20	1478	54
      // R3	18	17	1261	46
      // R4	13	46	1300	48
    },
  ],
];

const chartsData = ref([
  {
    label: "基站数量的影响",
    name: "first",
    chart: rawData[0].map((item) => {
      return generateOptions(item);
    }),
  },
  {
    label: "虚拟机数量的影响",
    name: "second",
    chart: rawData[1].map((item) => {
      return generateOptions(item);
    }),
  },
  {
    label: "物联网应用数量的影响",
    name: "third",
    chart: rawData[2].map((item) => {
      return generateOptions(item);
    }),
  },
  {
    label: "物联网应用截止时间的影响",
    name: "fourth",
    chart: rawData[3].map((item) => {
      return generateOptions(item);
    }),
  },
]);
</script>

<template>
  <div class="flex w-full h-full">
    <div
      class="flex flex-col justify-center items-center w-full max-w-[20%] border h-full"
      style="background: #fafafa"
      id="scrollbar"
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
          v-for="(item, index) in buttonData"
          :key="index"
          :class="[
            'flex place-content-center items-center bg-' +
              item.color +
              '-500 hover:bg-' +
              item.color +
              '-600 active:bg-' +
              item.color +
              '-700 h-fit p-2 rounded-3xl space-x-1',
          ]"
          @click="item.click"
        >
          <font-awesome-icon :icon="item.icon" class="h-4 w-4" />
          <span class="sm:invisible md:visible">{{ item.text }}</span>
        </button>
      </div>
    </div>

    <div class="px-8 pt-2 h-full">
      <div>
        <span> 算法选择： </span>
        <button
          v-for="(item, index) in algorithmList"
          :key="index"
          :class="[
            'px-4 py-2 m-2 rounded-2xl',
            selectedAlgorithmList.includes(item)
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200',
          ]"
          @click="toggleAlgorithm(item)"
        >
          {{ item }}
        </button>
      </div>

      <div>
        <span> 变量分析： </span>
        <button
          v-for="(item, index) in chartsData"
          :key="index"
          :class="[
            'px-4 py-2 m-2 rounded-2xl',
            activeName === item.name ? 'bg-blue-500 text-white' : 'bg-gray-200',
          ]"
          @click="toggleVariable(item.name)"
        >
          {{ item.label }}
        </button>
      </div>

      <div
        v-for="(item, index) in chartsData"
        :key="index"
        :label="item.label"
        :name="item.name"
        class="h-[100%]"
      >
        <template v-if="activeName === item.name">
          <div class="flex flex-row flex-wrap justify-between h-full">
            <div
              v-for="(_, index_) in 4"
              :style="{
                width: chartsWidth + 'px',
                height: chartsHeight + 'px',
              }"
              :key="index"
              class="p-4 m-4 border-2 rounded-2xl"
            >
              <v-chart
                :ref="(el) => (EchartsRef[index * 4 + index_] = el)"
                :option="item.chart[index_]"
                class="h-full w-full"
              />
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
