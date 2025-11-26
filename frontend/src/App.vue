<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

// --- State Management ---
const textToSummarize = ref('')
const summaryResult = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

// --- API Communication ---
const getSummary = async () => {
  isLoading.value = true
  errorMessage.value = ''
  summaryResult.value = ''

  // Client-side validation to prevent unnecessary API calls
  if (!textToSummarize.value || !textToSummarize.value.trim()) {
    errorMessage.value = 'Text field cannot be empty or contain only spaces.'
    isLoading.value = false
    return
  }

  const apiEndpoint = 'http://127.0.0.1:8000/summarize'
  const payload = {
    text: textToSummarize.value
  }

  try {
    const response = await axios.post(apiEndpoint, payload)
    summaryResult.value = response.data.summary
  } catch (error: any) {
    if (axios.isAxiosError(error) && error.response) {
      // Handle structured API errors from the backend
      const detail = error.response.data.detail
      if (typeof detail === 'string') {
        errorMessage.value = detail
      } else if (Array.isArray(detail)) {
        // Prettify Pydantic's validation error messages
        const pydanticError = detail[0]
        if (pydanticError.msg.includes('String should match pattern')) {
          errorMessage.value = 'The text field cannot be empty or contain only spaces.'
        } else {
          errorMessage.value = detail.map((d) => `${d.loc[1]}: ${d.msg}`).join(', ')
        }
      } else {
        errorMessage.value = 'An unexpected API error occurred.'
      }
    } else {
      // Handle network errors or other client-side issues
      errorMessage.value = 'A network error occurred. Is the backend server running?'
      console.error(error)
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <main class="container">
    <header>
      <h1>AI Text Summarizer</h1>
      <p>
        Paste your text below to get a concise summary using the Gemini API.
      </p>
    </header>

    <form @submit.prevent="getSummary">
      <textarea
        v-model="textToSummarize"
        placeholder="Enter a long piece of text here..."
        rows="10"
        required
      ></textarea>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Summarizing...' : 'Summarize' }}
      </button>
    </form>

    <div v-if="isLoading" class="loading-spinner"></div>

    <div v-if="errorMessage" class="result error">
      <h2>Error</h2>
      <p>{{ errorMessage }}</p>
    </div>

    <div v-if="summaryResult" class="result">
      <h2>Summary</h2>
      <p>{{ summaryResult }}</p>
    </div>
  </main>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #333;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

header {
  text-align: center;
  margin-bottom: 2rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
}

p {
  color: #555;
  line-height: 1.6;
}

form {
  display: flex;
  flex-direction: column;
}

textarea {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid #ddd;
  resize: vertical;
  margin-bottom: 1rem;
  transition: border-color 0.3s;
}

textarea:focus {
  outline: none;
  border-color: #42b883;
}

button {
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #42b883;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  align-self: flex-end;
}

button:hover:not(:disabled) {
  background-color: #35a06e;
}

button:disabled {
  background-color: #a5d8bf;
  cursor: not-allowed;
}

.result {
  margin-top: 2rem;
  padding: 1.5rem;
  border-radius: 8px;
  background-color: #fff;
  border: 1px solid #eee;
}

.result h2 {
  margin-bottom: 1rem;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.result.error {
  background-color: #fff5f5;
  border-color: #fecaca;
}

.result.error h2 {
  color: #c53030;
}

.result.error p {
  color: #c53030;
}

.loading-spinner {
  display: block;
  width: 40px;
  height: 40px;
  margin: 2rem auto;
  border: 4px solid #42b883;
  border-top: 4px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
