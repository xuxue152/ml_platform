<template>
  <div class="management-container">
    <div class="management-header">
      <div class="left-ops">
        <button @click="fetchDataset" class="refresh-btn">刷新数据</button>
        <button @click="toggleSelectAll" class="refresh-btn">全选/取消全选</button>
      </div>
      <div class="global-ops">
        <button @click="showGlobalDialog = true">全局操作</button>
        <button @click="showFillDialog = true">填充缺失</button>
      </div>
    </div>

    <div class="card-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="pagedData.length === 0" class="empty-state">
        <p>暂无数据</p>
      </div>

      <div v-else class="table-wrapper">
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th></th>
                <th v-for="(header, index) in tableHeaders" :key="index">
                  <input type="checkbox" v-model="selectedFeatures" :value="header" />
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, rowIndex) in pagedData" :key="rowIndex">
                <td></td>
                <td v-for="(value, colIndex) in row" :key="colIndex">{{ value }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="operation-panel">
          <select v-model="selectedOperation">
            <option disabled value="">选择操作</option>
            <option v-for="(label, op) in featureOperations" :key="op" :value="op">
              {{ label }}
            </option>
          </select>
          <button @click="applyOperation">应用</button>
          <button class="finish-btn" @click="goBackToDatasetList">完成修改</button>
        </div>


        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
          <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        </div>
      </div>
    </div>

    <!-- 全局操作浮窗 -->
    <div v-if="showGlobalDialog" class="dialog-overlay">
      <div class="dialog">
        <h3>选择全局操作</h3>
        <button @click="() => { applyGlobal('drop_duplicates'); showGlobalDialog = false }">删除重复值</button>
        <button @click="() => { applyGlobal('drop_high_missing'); showGlobalDialog = false }">删除高缺失</button>
        <button @click="() => { applyGlobal('drop_low_variance'); showGlobalDialog = false }">删除低方差</button>
        <button @click="showGlobalDialog = false">关闭</button>
      </div>
    </div>

    <!-- 缺失值填充浮窗 -->
    <div v-if="showFillDialog" class="dialog-overlay">
      <div class="dialog">
        <h3>选择填充方式</h3>
        <button @click="() => { applyFill('fill_mean'); showFillDialog = false }">均值填充</button>
        <button @click="() => { applyFill('fill_median'); showFillDialog = false }">中位数填充</button>
        <button @click="() => { applyFill('fill_mode'); showFillDialog = false }">众数填充</button>
        <button @click="showFillDialog = false">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const datasetName = route.params.dataset_name
const userId = localStorage.getItem('user_id')
const projectName = localStorage.getItem('projectName')  // 获取项目名

const allData = ref([])
const tableHeaders = ref([])
const loading = ref(true)
const currentPage = ref(1)
const pageSize = 10
const selectedFeatures = ref([])
const selectedOperation = ref('')
const showGlobalDialog = ref(false)
const showFillDialog = ref(false)

const totalPages = computed(() => Math.ceil(allData.value.length / pageSize))

const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return allData.value.slice(start, start + pageSize)
})
const reloadOps = new Set([
  'drop',
  'datetime_extraction',
  'drop_duplicates',
  'drop_high_missing',
  'drop_low_variance',
  'target_encoding',
  'pca',
  'one_hot'
])
const featureOperations = {
  drop: '删除特征',
  remove_outliers: '删除异常值',
  one_hot: '独热编码',
  label_encode: '标签编码',
  standardize: '标准化',
  normalize: '归一化',
  robust_scale: '鲁棒缩放',
  log_transform: '对数变换',
  binning: '分箱',
  pca: '降维',
  handle_skewness: '处理偏态',
  datetime_extraction: '时间提取',
  text_length: '转为长度',
  interaction_terms: '交互特征',
  polynomial_features: '转为平方',
  target_encoding: '目标编码',
}

const toggleSelectAll = () => {
  if (selectedFeatures.value.length === tableHeaders.value.length) {
    selectedFeatures.value = []
  } else {
    selectedFeatures.value = [...tableHeaders.value]
  }
}

const fetchDataset = async () => {
  loading.value = true
  try {
    const response = await axios.post(`http://localhost:8000/api/datasets/${datasetName}/show_dataset`, {
      user_id: userId,
      name: datasetName
    })
    allData.value = response.data
    if (response.data.length > 0) {
      tableHeaders.value = Object.keys(response.data[0])
    }
  } catch (err) {
    console.error('获取数据失败:', err)
  } finally {
    loading.value = false
  }
}

const applyOperation = async () => {
  if (!selectedOperation.value || selectedFeatures.value.length === 0) return
  const operation = {
    operation: selectedOperation.value,
    args: [selectedFeatures.value]
  }
  await applyMeasures([operation])
}

const applyGlobal = async (opName) => {
  await applyMeasures([{ operation: opName }])
  showGlobalDialog.value = false
}

const applyFill = async (fillOp) => {
  const ops = selectedFeatures.value.map(col => ({ operation: fillOp, args: [col] }))
  await applyMeasures(ops)
  showFillDialog.value = false
}

const applyMeasures = async (measures) => {
  try {
    await axios.post(`http://localhost:8000/api/datasets/${datasetName}/alter_dataset`, {
      name: datasetName,
      user_id: userId,
      measures
    })
    // 获取所有操作名
    const ops = measures.map(m => m.operation)
    const shouldReload = ops.some(op => reloadOps.has(op))

    if (shouldReload) {
      location.reload()
    } else {
      await fetchDataset()
    }
  } catch (err) {
    console.error('操作失败:', err)
    alert(`操作失败: ${err.response?.data?.detail || err.message}`)
  }
}

const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }

const goBackToDatasetList = () => {
  if (projectName) {
    router.push(`/projects/${projectName}/datasets`)
  } else {
    alert('项目名不存在，请检查 localStorage 中的 projectName')
  }
}

onMounted(fetchDataset)
</script>


<style scoped>
.management-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}
.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}
.refresh-btn {
  background-color: #edf2f7;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.left-ops {
  display: flex;
  gap: 1rem;
}
.global-ops {
  display: flex;
  gap: 1rem;
}
.table-wrapper {
  overflow-x: auto;
}
.table-responsive {
  min-width: 600px;
  overflow-x: auto;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
}
.data-table th, .data-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
  white-space: nowrap;
}
.operation-panel {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  align-items: center;
}
.pagination {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
  align-items: center;
}
.dialog-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}
.dialog {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
  min-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.finish-btn {
  background-color: #3182ce; /* 蓝色主色 */
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  float: right; /* 将按钮推到容器右侧 */
  margin-left: auto;
}
.finish-btn:hover {
  background-color: #2b6cb0; /* 蓝色 hover 变深 */
}

</style>
