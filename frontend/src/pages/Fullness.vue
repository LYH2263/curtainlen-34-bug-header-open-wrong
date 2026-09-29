<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const loss = ref('0'); const msg = ref('')
onMounted(async () => { const s = await getJSON('/api/settings'); loss.value = s.header_tape_joint_loss ?? '0' })
async function save(){
  msg.value = ''
  try {
    await postJSON('/api/settings', { key: 'header_tape_joint_loss', value: String(loss.value) })
    msg.value = '已保存'
  } catch(e){ msg.value = e.message }
}
</script>
<template><div class="page"><h1>褶倍说明</h1><p>成品宽 = 窗宽 × 褶倍；幅数 = ceil(成品宽 / 门幅)。</p>
<h2>帘头带默认接头损耗</h2>
<p><input type="number" step="0.01" min="0" v-model="loss"> m <button @click="save">保存</button></p>
<p>{{ msg }}</p>
</div></template>
