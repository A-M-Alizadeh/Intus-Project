<template>
  <div class="card">
    <h3>{{ title }}</h3>
    <div class="black-viewer">
      <img v-if="imageSrc" :src="imageSrc" />
      <span v-else>Nessuna immagine</span>
    </div>
  </div>
</template>

<script setup>
defineProps(['title', 'imageSrc']);
</script>

<style scoped>
.card { background: white; padding: 1.5rem; border-radius: 12px; flex: 1; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
h3 { color: #1e293b; margin: 0 0 1.2rem 0; font-size: 1.1rem; }
.black-viewer { 
  background: #000; 
  height: 320px; 
  border-radius: 8px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  overflow: hidden;
  color: #94a3b8;
}
img { max-width: 100%; max-height: 100%; object-fit: contain; }
</style>