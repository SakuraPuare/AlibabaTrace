<script setup>
import Header from "../components/Header.vue";
import ToTop from "../components/tools/ToTop.vue";
import Tree from "../components/tools/Tree.vue";
import http from "../../utils/http.js";
import {onMounted, ref} from "vue";
import {getColumnDetails} from "../../utils/utils.js";

const TreeData = ref([]);
const selectedItem = ref({})
const getTreeData = () => {
  http.get('/table/tree').then(
      res => {
        // clear data
        TreeData.value = []

        let data = res.data.data
        for (let key in data) {
          let children = [];
          for (let file in data[key].files) {
            children.push({
              id: file,
              path: [
                data[key].name,
                data[key].files[file]
              ],
              label: data[key].files[file],
              children: [],
            })
          }
          TreeData.value.push({
            id: key,
            path: [data[key].name],
            label: data[key].name,
            children: children,
            disabled: true
          })
        }
        // sort
        TreeData.value.sort((a, b) => {
          return b.label.localeCompare(a.label, 'zh')
        })
        for (let key in TreeData.value) {
          TreeData.value[key].children.sort((a, b) => {
            return a.label.localeCompare(b.label)
          })
        }
      }
  ).catch(
      err => {
        console.log(err)
      }
  )
}

const TablePage = ref(1)
const TableData = ref([])
// const TableDataPage = ref({})
const TableColumns = ref([])

const getTableData = (name, page = 1) => {
  http.get('/table/' + name, {
    params: {
      page: page
    }
  }).then(
      res => {
        TableData.value = []
        const data = res.data.data
        for (let i = 0; i < data.length; i++) {
          let row = data[i].split(',')
          let obj = {}
          for (let j = 0; j < row.length; j++) {
            obj[TableColumns.value[j].dataKey] = row[j]
          }
          TableData.value.push(obj)
        }
        // TableDataPage.value[page] = ret
        // for i in TableDataPage.value
        // for (let i in TableDataPage.value) {
        //   TableData.value = TableData.value.concat(TableDataPage.value[i])
        // }
      }
  ).catch(
      err => {
        console.log(err)
      }
  )
}

const getSelect = (data) => {
  console.log(data)
  selectedItem.value = data
  if (data.path?.length > 0) {
    TableColumns.value = getColumnDetails(data.path)
    getTableData(data.id, TablePage.value++)
  }
  else{
    TableColumns.value = []
    TableData.value = []
  }

}

// const generateColumns = (length = 10, prefix = 'column-', props = {}) =>
//     Array.from({length}).map((_, columnIndex) => ({
//       ...props,
//       key: `${prefix}${columnIndex}`,
//       dataKey: `${prefix}${columnIndex}`,
//       title: `Column ${columnIndex}`,
//       width: 150,
//     }))
// const generateData = (columns, length = 200, prefix = 'row-') =>
//     Array.from({length}).map((_, rowIndex) => {
//       return columns.reduce((rowData, column, columnIndex) => {
//         rowData[column.dataKey] = `Row ${rowIndex} - Col ${columnIndex}`
//         return rowData
//       }, {
//         id: `${prefix}${rowIndex}`,
//         parentId: null,
//       })
//     })
// const columns = generateColumns(10)
// const data = generateData(columns, 100)
// console.log(data)
// const ContainerHeight = ref(0)

// const updateHeight = () => {
//   ContainerHeight.value = getHeightWithoutHeader();
// };

onMounted(() => {
  getTreeData()
  // updateHeight()
  // window.addEventListener('resize', updateHeight);
})

// onUnmounted(() => {
//   window.removeEventListener('resize', updateHeight);
// })
</script>


<template>
  <Header/>
  <div class="flex w-full h-full">
    <div class="flex flex-col justify-center items-center w-full max-w-[20%] h-full"
         style="background: #fafafa;">
      <Tree :data="TreeData" @select="getSelect"/>
    </div>
    <div class="flex flex-col max-h-full mx-32 w-full pt-16">
      <div class="w-full h-full">
        <el-auto-resizer>
          <template #default="{ height, width }">
            <el-table-v2
                stimated-row-height
                :columns="TableColumns"
                :data="TableData"
                :height="height"
                :width="width"/>
          </template>
        </el-auto-resizer>
      </div>
    </div>
  </div>
  <ToTop/>
</template>

<style scoped>

</style>
