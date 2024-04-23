<script setup>
import { onMounted, ref } from "vue";
import VChart from "vue-echarts";
import * as echarts from "echarts";
import axios from "axios";
import { getHeightWithoutHeader } from "../utils/utils.js";

const cpu = ref([]);
const mem = ref([]);
const heatmap = ref([]);

const net_in = ref([]);
const net_out = ref([]);
const disk_io_percent = ref([]);
const cpu_util_percent = ref([]);
const mem_util_percent = ref([]);
const lines = ref([]);

const scatter = ref([]);

onMounted(() => {
  axios.get("/heatmap.json").then((response) => {
    cpu.value = response.data.cpu;
    mem.value = response.data.mem;
    heatmap.value = response.data.data;
  });
  axios.get("/lines.json").then((response) => {
    lines.value = response.data.time;
    net_in.value = response.data.net_in;
    net_out.value = response.data.net_out;
    disk_io_percent.value = response.data.disk_io_percent;
    cpu_util_percent.value = response.data.cpu_util_percent;
    mem_util_percent.value = response.data.mem_util_percent;
  });
  axios.get("/scatter.json").then((response) => {
    scatter.value = response.data;
  });
});

const chartsData = ref([
  {
    title: {
      text: "任务执行时间分布图",
    },
    xAxis: {
      data: [
        "1.00-1.95",
        "1.95-2.90",
        "2.90-3.85",
        "3.85-4.80",
        "4.80-5.75",
        "5.75-6.70",
        "6.70-7.65",
        "7.65-8.60",
        "8.60-9.55",
        "9.55-10.50",
        "10.50-11.45",
        "11.45-12.40",
        "12.40-13.35",
        "13.35-14.30",
        "14.30-15.25",
        "15.25-16.20",
        "16.20-17.15",
        "17.15-18.10",
        "18.10-19.05",
        "19.05-20.00",
      ],
      axisLabel: {
        inside: true,
        color: "#fff",
      },
      axisTick: {
        show: false,
      },
      axisLine: {
        show: false,
      },
      z: 10,
    },
    yAxis: {
      axisLine: {
        show: false,
      },
      axisTick: {
        show: false,
      },
      axisLabel: {
        color: "#999",
      },
    },
    dataZoom: [
      {
        type: "inside",
      },
    ],
    series: [
      {
        type: "bar",
        showBackground: true,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#83bff6" },
            { offset: 0.5, color: "#188df0" },
            { offset: 1, color: "#188df0" },
          ]),
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "#2378f7" },
              { offset: 0.7, color: "#2378f7" },
              { offset: 1, color: "#83bff6" },
            ]),
          },
        },
        data: [
          3, 2, 2, 3, 1, 0, 4, 2, 5, 25, 63, 111, 125, 94, 41, 17, 6, 6, 2, 0,
        ],
      },
    ],
  },
  {
    title: {
      text: "任务CPU和内存使用情况",
    },
    tooltip: {},
    xAxis: {
      type: "category",
      data: cpu,
    },
    yAxis: {
      type: "category",
      data: mem,
    },
    visualMap: {
      min: 0,
      max: 1500,
      calculable: true,
      realtime: false,
      inRange: {
        color: [
          "#313695",
          "#4575b4",
          "#74add1",
          "#abd9e9",
          "#e0f3f8",
          "#ffffbf",
          "#fee090",
          "#fdae61",
          "#f46d43",
          "#d73027",
          "#a50026",
        ],
      },
    },
    series: [
      {
        name: "Gaussian",
        type: "heatmap",
        data: heatmap,
        emphasis: {
          itemStyle: {
            borderColor: "#333",
            borderWidth: 1,
          },
        },
        progressive: 1000,
        animation: false,
      },
    ],
  },
  {
    title: {
      text: "主机资源使用情况",
    },
    tooltip: {
      trigger: "axis",
    },
    legend: {
      data: [
        "net_in",
        "net_out",
        "disk_io_percent",
        "cpu_util_percent",
        "mem_util_percent",
      ],
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true,
    },
    toolbox: {
      feature: {
        saveAsImage: {},
      },
    },
    xAxis: {
      type: "category",
      boundaryGap: false,
      data: lines,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "net_in",
        type: "line",
        stack: "总量",
        data: net_in,
      },
      {
        name: "net_out",
        type: "line",
        stack: "总量",
        data: net_out,
      },
      {
        name: "disk_io_percent",
        type: "line",
        stack: "总量",
        data: disk_io_percent,
      },
      {
        name: "cpu_util_percent",
        type: "line",
        stack: "总量",
        data: cpu_util_percent,
      },
      {
        name: "mem_util_percent",
        type: "line",
        stack: "总量",
        data: mem_util_percent,
      },
    ],
  },
  {
    title: {
      text: "微服务各项资源访问时延",
      left: "center",
      top: 0,
    },
    visualMap: {
      min: 0,
      max: 0.0005,
      dimension: 1,
      orient: "vertical",
      right: 10,
      top: "center",
      text: ["HIGH", "LOW"],
      calculable: true,
      inRange: {
        color: ["#f2c31a", "#24b7f2"],
      },
    },
    tooltip: {
      trigger: "item",
      axisPointer: {
        type: "cross",
      },
    },
    xAxis: [
      {
        type: "value",
      },
    ],
    yAxis: [
      {
        type: "value",
      },
    ],
    series: [
      {
        name: "time",
        type: "scatter",
        symbolSize: 5,
        data: scatter,
      },
    ],
  },
]);

const chartsRef = ref([null, null]);

const height = getHeightWithoutHeader();
</script>

<template>
  <div
    class="flex flex-row flex-wrap container justify-around items-center w-full mx-auto"
  >
    <div
      v-for="(item, index) in chartsData"
      id="charts"
      :key="index"
      :ref="chartsRef[index]"
    >
      <div>{{ index }}</div>
      <v-chart
        :id="'charts_' + index"
        :option="item"
        :style="`height: ${height / 2 - 64}px; width: 600px`"
        autoresize
        class="chart"
      />
    </div>
  </div>
</template>

<style scoped></style>

<!--根据您的数据表定义，我提出以下几种可能的图表展示方式：-->

<!--1. **任务执行时间分布图**：使用`alibaba.batch_instance`表的`start_time`和`end_time`，我们可以展示各个任务的执行时间。这可以用柱状图或者箱线图来展示。-->

<!--2. **任务资源使用情况**：使用`alibaba.batch_instance`表的`cpu_avg`, `cpu_max`, `mem_avg`, `mem_max`，我们可以展示任务的CPU和内存使用情况。这可以用柱状图、线图或者热力图表示。-->

<!--3. **服务调用时延分布图**：使用`alibaba.call_graph`表的`rt`，我们可以展示服务调用的时延分布。这可以用直方图或者箱线图表示。-->

<!--4. **节点资源规格与使用情况对比**：使用`alibaba.container`表的`container_cpu_spec`, `container_mem_spec`，以及`alibaba.container_usage`表的`cpu_util_percent`, `mem_util_percent`，我们可以展示节点资源规格与实际使用情况的对比。这可以用柱状图或者堆叠柱状图表示。-->

<!--5. **主机资源使用情况**：使用`alibaba.machine_usage`表的`cpu_util_percent`, `mem_util_percent`，我们可以展示主机的资源使用情况。这可以用线图、面积图或者热力图表示。-->

<!--6. **微服务资源使用情况**：使用`alibaba.ms_metrics`表的`cpu_utilization`, `memory_utilization`，我们可以展示微服务的资源使用情况。这可以用线图、面积图或者热力图表示。-->

<!--7. **微服务各项资源访问时延**：使用`alibaba.ms_resource`表的`providerrpc_rt`, `consumerrpc_rt`, `writemc_rt`, `readmc_rt`, `writedb_rt`, `readdb_rt`, `consumermq_rt`, `providermq_rt`, `http_rt`，我们可以展示微服务各项资源访问的时延。这可以用柱状图、线图或者热力图表示。-->

<!--请注意，以上的图表类型选择和数据选择都是基于数据表定义，实际的图表选择还需要考虑您的具体需求和数据的实际分布情况。-->
<!--根据您提供的数据表定义，我提出以下几种可能的图表展示方式：-->

<!--1. **任务执行时间分布图**：使用`alibaba.batch_instance`表的`start_time`和`end_time`，我们可以展示各个任务的执行时间。这可以用柱状图或者箱线图来展示。-->

<!--2. **任务资源使用情况**：使用`alibaba.batch_instance`表的`cpu_avg`, `cpu_max`, `mem_avg`, `mem_max`，我们可以展示任务的CPU和内存使用情况。这可以用柱状图、线图或者热力图表示。-->

<!--3. **服务调用时延分布图**：使用`alibaba.call_graph`表的`rt`，我们可以展示服务调用的时延分布。这可以用直方图或者箱线图表示。-->

<!--4. **节点资源规格与使用情况对比**：使用`alibaba.container`表的`container_cpu_spec`, `container_mem_spec`，以及`alibaba.container_usage`表的`cpu_util_percent`, `mem_util_percent`，我们可以展示节点资源规格与实际使用情况的对比。这可以用柱状图或者堆叠柱状图表示。-->

<!--5. **主机资源使用情况**：使用`alibaba.machine_usage`表的`cpu_util_percent`, `mem_util_percent`，我们可以展示主机的资源使用情况。这可以用线图、面积图或者热力图表示。-->

<!--6. **微服务资源使用情况**：使用`alibaba.ms_metrics`表的`cpu_utilization`, `memory_utilization`，我们可以展示微服务的资源使用情况。这可以用线图、面积图或者热力图表示。-->

<!--7. **微服务各项资源访问时延**：使用`alibaba.ms_resource`表的`providerrpc_rt`, `consumerrpc_rt`, `writemc_rt`, `readmc_rt`, `writedb_rt`, `readdb_rt`, `consumermq_rt`, `providermq_rt`, `http_rt`，我们可以展示微服务各项资源访问的时延。这可以用柱状图、线图或者热力图表示。-->

<!--8. **主机内存和CPU规格**：使用`alibaba.machine_meta`表的`cpu_num`和`mem_size`，我们可以展示每台主机的内存和CPU规格。这可以用柱状图表示。-->

<!--9. **容器的CPU和内存请求**：使用`alibaba.container_meta`表的`cpu_request`和`mem_size`，我们可以展示每个容器的CPU和内存请求。这可以用柱状图表示。-->

<!--10. **节点的CPU和内存利用率**：使用`alibaba.node`表的`cpu_utilization`和`memory_utilization`，我们可以展示每个节点的CPU和内存利用率。这可以用线图或者热力图表示。-->

<!--以上的图表类型选择和数据选择都是基于数据表定义，实际的图表选择还需要考虑您的具体需求和数据的实际分布情况。-->
