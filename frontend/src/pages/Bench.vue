<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const wid = ref(1); const fid = ref(1); const out = ref(null)
const tape = ref(false); const loss = ref('0'); const err = ref('')
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  const s = await getJSON('/api/settings')
  loss.value = s.header_tape_joint_loss ?? '0'
})
function params(){
  const p = { window_id: wid.value, fabric_id: fid.value, header_tape: tape.value }
  if (tape.value && loss.value !== '' && loss.value != null) p.joint_loss = Number(loss.value)
  return p
}
async function go(save){
  err.value = ''
  try {
    if (save) {
      out.value = await postJSON('/api/estimate', { ...params(), save: true })
    } else {
      const p = params()
      let q = `/api/estimate?window_id=${p.window_id}&fabric_id=${p.fabric_id}&header_tape=${p.header_tape}`
      if (p.joint_loss != null) q += `&joint_loss=${p.joint_loss}`
      out.value = await getJSON(q)
    }
  } catch(e){ err.value = e.message }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<label><input type="checkbox" v-model="tape"> 帘头带</label>
<label v-if="tape">接头损耗(m) <input type="number" step="0.01" min="0" v-model="loss"></label>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="err" class="bad">{{ err }}</p>
<PanelCut v-if="out" :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" />
<p v-if="out && out.header_tape">帘头带 {{ out.header_tape_meters }} m（含接头损耗 {{ out.header_tape_joint_loss }} m）</p>
</div></template>
