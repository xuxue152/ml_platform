<template>
  <div class="management-container">
    <div class="management-header">
      <button @click="fetchDataset" class="refresh-btn">刷新数据</button>
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
                <th v-for="(header, index) in tableHeaders" :key="index">{{ header }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, rowIndex) in pagedData" :key="rowIndex">
                <td v-for="(value, colIndex) in row" :key="colIndex">{{ value }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
          <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const projectName = route.params.project_name
const datasetName = route.params.dataset_name
const userId = parseInt(localStorage.getItem('user_id'))

const allData = ref([])
const tableHeaders = ref([])
const loading = ref(true)
const currentPage = ref(1)
const pageSize = 10

const totalPages = computed(() => Math.ceil(allData.value.length / pageSize))

const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return allData.value.slice(start, start + pageSize)
})

const fetchDataset = async () => {
  loading.value = true
  try {
    const response = await axios.post(`http://localhost:8000/api/${projectName}/datasets/${datasetName}/show_dataset`, {
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

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
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

.card-container {
  padding-top: 1rem;
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

.pagination {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
  align-items: center;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 2rem 0;
}
</style>
