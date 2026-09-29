<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([]); const openId = ref(''); const detail = ref(null); const err = ref('')
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
async function open(id){
  err.value = ''; detail.value = null
  try { detail.value = await getJSON(`/api/runs/${id}`) } catch(e){ err.value = e.message }
}
function listTape(r){
  // Prefer list pin chip; fall back to primary meters.
  const pin = r.result?.list_header_tape_meters
  if (pin != null) return pin
  return r.result?.header_tape_meters
}
function detailTape(d){
  return d?.result?.header_tape_meters
}
</script>
<template><div class="page"><h1>记录</h1>
<p><input v-model="openId" placeholder="编号"> <button @click="open(openId)">打开</button></p>
<p v-if="err" class="bad">{{ err }}</p>
<div v-if="detail">
  <h2>#{{ detail.id }} {{ detail.window_name }} / {{ detail.fabric_name }}</h2>
  <p>主帘 {{ detail.result?.meters }} m（{{ detail.result?.panels }} 幅 × {{ detail.result?.cut_height }} m）</p>
  <p v-if="detail.result?.header_tape">帘头带 {{ detailTape(detail) }} m（含接头损耗 {{ detail.result.header_tape_joint_loss }} m）</p>
  <p v-else>未开帘头带</p>
</div>
<ul><li v-for="r in items" :key="r.id">
  <a href="#" @click.prevent="open(r.id)">#{{ r.id }}</a> {{ r.window_name }} {{ r.result?.meters }}m
  <span v-if="r.result?.header_tape"> ＋帘头带 {{ listTape(r) }}m</span>
</li></ul>
<p class="hint">列表用 pin 字段展示帘头带；详情用主字段。改褶量默认损耗后再打开旧编号。</p>
</div></template>
