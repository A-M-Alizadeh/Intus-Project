<script setup>
import { ref } from 'vue';
import ControlPanel from './components/ControlPanel.vue';
import ImageCard from './components/ImageCard.vue';

const originalUrl = ref(null);
const processedUrl = ref(null);
const statusMsg = ref("");
const isDone = ref(false);
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

/**
 * Save the local preview URL for the original image selected by the user.
 */
const handlePreview = (url) => {
  originalUrl.value = url;
};

/**
 * Send image + phase to the backend and store the processed image response.
 */
const processOnServer = async (formData) => {
  statusMsg.value = "In elaborazione...";
  isDone.value = false;
  try {
    // The backend handles image processing entirely.
    const response = await fetch(`${API_BASE_URL}/api/imaging/process/`, {
      method: "POST",
      body: formData
    });
    
    if (!response.ok) throw new Error("Errore del server");
    
    const data = await response.json();
    processedUrl.value = `data:image/png;base64,${data.processed}`;
    statusMsg.value = "Elaborazione completata";
    isDone.value = true;
  } catch (e) {
    statusMsg.value = "❌ Errore di connessione";
    isDone.value = false;
  }
};
</script>

<template>
  <div class="main-layout">
    <div class="centered-content">
      <h1 class="page-title">Medical Phase Simulator</h1>
      
      <ControlPanel 
        @preview="handlePreview" 
        @process="processOnServer" 
      />

      <div class="comparison-grid">
        <ImageCard title="Originale" :imageSrc="originalUrl" />
        <ImageCard title="Elaborata" :imageSrc="processedUrl" />
      </div>

      <div v-if="statusMsg" class="status-footer" :class="{ done: isDone, error: !isDone }">
        <span>{{ isDone ? "✅" : "⚠️" }}</span> {{ statusMsg }}
      </div>
    </div>
  </div>
</template>

<style>
body { margin: 0; background-color: #f1f5f9; font-family: 'Inter', sans-serif; }

.main-layout {
  display: flex;
  justify-content: center; /* Centers horizontally */
  width: 100%;
  min-height: 100vh;
}

.centered-content {
  width: 95%;
  max-width: 1100px; /* Limits width for a professional look */
  display: flex;
  flex-direction: column;
  align-items: center; /* Centers children like the title and bar */
  padding: 3rem 0;
}

.page-title {
  color: #1e293b;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
}

.comparison-grid {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 2rem;
  width: 100%;
  margin-top: 1rem;
}

.status-footer {
  margin-top: 2rem;
  font-weight: 600;
}

.status-footer.done {
  color: #10b981;
}

.status-footer.error {
  color: #dc2626;
}
</style>