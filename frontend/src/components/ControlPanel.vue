<script setup>
import { ref } from 'vue';

const emit = defineEmits(['process', 'preview']);
const fileName = ref("Nessun file selezionato");

/**
 * Read the selected file, update label text, and emit a local preview URL.
 */
const onFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    fileName.value = file.name;
    // Sends a local preview URL to App.vue for the "Originale" panel.
    emit('preview', URL.createObjectURL(file));
  }
};

/**
 * Build FormData from the form and ask the parent to process it on backend.
 */
const handleSubmit = (event) => {
  const formElement = event.target;
  const formData = new FormData(formElement);
  // Sends image + phase selection to the Django backend.
  emit('process', formData);
};
</script>

<template>
  <div class="controls-card">
    <form @submit.prevent="handleSubmit" class="bar-layout">
      <div class="file-section">
        <label for="file-upload" class="btn-outline">Scegli file</label>
        <input 
          id="file-upload" 
          type="file" 
          name="image" 
          accept="image/png,image/jpeg"
          @change="onFileChange" 
          hidden 
          required 
        />
        <span class="file-name">{{ fileName }}</span>
      </div>

      <div class="radio-group">
        <label class="radio-label">
          <input type="radio" name="phase" value="arterial" checked /> 
          <span>Arteriosa</span>
        </label>
        <label class="radio-label">
          <input type="radio" name="phase" value="venous" /> 
          <span>Venosa</span>
        </label>
      </div>

      <button type="submit" class="btn-blue">Elabora immagine</button>
    </form>
  </div>
</template>

<style scoped>
.controls-card {
  background: white;
  width: 100%;
  padding: 1rem 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
  box-sizing: border-box;
}
.bar-layout {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.file-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #64748b;
}
.radio-group {
  display: flex;
  gap: 1.5rem;
}
.radio-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #1e293b;
  font-weight: 500;
  cursor: pointer;
}
.btn-blue {
  background: #0066ff;
  color: white;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}
.btn-outline {
  border: 1px solid #cbd5e1;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  background: #fff;
  font-size: 0.9rem;
}
.file-name {
  font-size: 0.85rem;
  color: #64748b;
}
</style>