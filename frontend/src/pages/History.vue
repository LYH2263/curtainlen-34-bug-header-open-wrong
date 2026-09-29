<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([]); const openId = ref(''); const detail = ref(null); const err = ref('')
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
async function open(id){
  err.value = ''; detail.value = null
  try { detail.value = await getJSON(`/api/runs/${id}`) } catch(e){ err.value = e.message }
}
function tapeMeters(r){
  // 列表与详情同读写入时冻结的带长，不使用 pin 字段。
  return r?.result?.header_tape_meters
}
</script>
<template><div class="page"><h1>记录</h1>
<p><input v-model="openId" placeholder="编号"> <button @click="open(openId)">打开</button></p>
<p v-if="err" class="bad">{{ err }}</p>
<div v-if="detail">
  <h2>#{{ detail.id }} {{ detail.window_name }} / {{ detail.fabric_name }}</h2>
  <p>主帘 {{ detail.result?.meters }} m（{{ detail.result?.panels }} 幅 × {{ detail.result?.cut_height }} m）</p>
  <p v-if="detail.result?.header_tape">帘头带 {{ tapeMeters(detail) }} m（含接头损耗 {{ detail.result.header_tape_joint_loss }} m）</p>
  <p v-else>未开帘头带</p>
</div>
<ul><li v-for="r in items" :key="r.id">
  <a href="#" @click.prevent="open(r.id)">#{{ r.id }}</a> {{ r.window_name }} {{ r.result?.meters }}m
  <span v-if="r.result?.header_tape"> ＋帘头带 {{ tapeMeters(r) }}m</span>
</li></ul>
<p class="hint">列表摘要与详情同为写入时固化的带长与主帘米；改褶量默认损耗后再打开旧编号，数值仍钉在快照上。</p>
</div></template>
