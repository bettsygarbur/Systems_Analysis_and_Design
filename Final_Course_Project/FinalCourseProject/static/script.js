// Variables globales
let selectedFile = null;
let predictions = [];

// Elementos del DOM
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const predictBtn = document.getElementById('predictBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const loadingText = document.getElementById('loadingText');
const predictionsSection = document.getElementById('predictionsSection');
const tableBody = document.getElementById('tableBody');
const downloadBtn = document.getElementById('downloadBtn');

// Event Listeners para upload
uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('active');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('active');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('active');
    handleFile(e.dataTransfer.files[0]);
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Cargar archivo
function handleFile(file) {
    if (!file) return;
    
    if (!file.name.endsWith('.csv') && !file.name.endsWith('.parquet')) {
        showError('Solo se aceptan archivos CSV o Parquet');
        return;
    }
    
    selectedFile = file;
    uploadArea.innerHTML = `
        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <p><strong>${file.name}</strong> seleccionado</p>
        <p style="color: #64748b; font-size: 0.9em;">Tamaño: ${(file.size / 1024 / 1024).toFixed(2)} MB</p>
    `;
    predictBtn.disabled = false;
}

// Realizar predicción
predictBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    showLoading('Enviando archivo y entrenando modelo...');
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error en la predicción');
        }
        
        const data = await response.json();
        predictions = data.predictions;
        
        // Mostrar resultados
        displayPredictions(data);
        loadMetrics();
        loadFeatureImportance();
        
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        hideLoading();
    }
});

// Mostrar predicciones
function displayPredictions(data) {
    predictionsSection.style.display = 'block';
    
    // Actualizar resumen
    document.getElementById('recordsProcessed').textContent = data.records_processed;
    document.getElementById('recordsCount').textContent = `${data.records_processed} registros`;
    
    const positiveCount = predictions.filter(p => p.prediction === 1).length;
    const negativeCount = predictions.filter(p => p.prediction === 0).length;
    
    document.getElementById('positiveCount').textContent = positiveCount;
    document.getElementById('negativeCount').textContent = negativeCount;
    
    // Llenar tabla
    tableBody.innerHTML = '';
    predictions.forEach(pred => {
        const row = document.createElement('tr');
        const predictionText = pred.prediction === 1 ? 'Sí (Problemático)' : 'No (Normal)';
        const badgeClass = pred.prediction === 1 ? 'badge-positive' : 'badge-negative';
        
        row.innerHTML = `
            <td>${pred.id}</td>
            <td><span class="prediction-badge ${badgeClass}">${predictionText}</span></td>
            <td>${(pred.probability_class_0 * 100).toFixed(2)}%</td>
            <td>${(pred.probability_class_1 * 100).toFixed(2)}%</td>
            <td>${(pred.confidence * 100).toFixed(2)}%</td>
        `;
        tableBody.appendChild(row);
    });
    
    // Scroll a resultados
    predictionsSection.scrollIntoView({ behavior: 'smooth' });
}

// Cargar métricas
async function loadMetrics() {
    try {
        const response = await fetch('/api/metrics');
        const data = await response.json();
        
        if (data.status === 'success') {
            document.getElementById('metric-accuracy').textContent = 
                (data.metrics.accuracy * 100).toFixed(2) + '%';
            document.getElementById('metric-precision').textContent = 
                (data.metrics.precision * 100).toFixed(2) + '%';
            document.getElementById('metric-recall').textContent = 
                (data.metrics.recall * 100).toFixed(2) + '%';
            document.getElementById('metric-f1').textContent = 
                (data.metrics.f1 * 100).toFixed(2) + '%';
            document.getElementById('metric-roc_auc').textContent = 
                (data.metrics.roc_auc * 100).toFixed(2) + '%';
        }
    } catch (error) {
        console.error('Error cargando métricas:', error);
    }
}

// Cargar importancia de características
async function loadFeatureImportance() {
    try {
        const response = await fetch('/api/feature-importance');
        const data = await response.json();
        
        if (data.status === 'success') {
            const chart = document.getElementById('importanceChart');
            chart.innerHTML = '';
            
            // Normalizar valores para mejor visualización
            const maxImportance = Math.max(...data.importance);
            
            data.features.forEach((feature, index) => {
                const importance = data.importance[index];
                const percentaje = (importance / maxImportance) * 100;
                
                const item = document.createElement('div');
                item.className = 'importance-item';
                item.innerHTML = `
                    <div class="importance-label" title="${feature}">${feature}</div>
                    <div class="importance-bar" style="width: ${percentaje * 0.8 + 20}%">
                        <span class="importance-value">${importance.toFixed(1)}</span>
                    </div>
                `;
                chart.appendChild(item);
            });
        }
    } catch (error) {
        console.error('Error cargando importancia:', error);
    }
}

// Descargar resultados
downloadBtn.addEventListener('click', () => {
    if (predictions.length === 0) return;
    
    // Crear CSV
    let csv = 'ID,Predicción,Probabilidad_No,Probabilidad_Sí,Confianza\n';
    predictions.forEach(pred => {
        const predictionText = pred.prediction === 1 ? 'Sí' : 'No';
        csv += `${pred.id},${predictionText},${(pred.probability_class_0 * 100).toFixed(2)},${(pred.probability_class_1 * 100).toFixed(2)},${(pred.confidence * 100).toFixed(2)}\n`;
    });
    
    // Descargar
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'predicciones_' + new Date().getTime() + '.csv';
    a.click();
    window.URL.revokeObjectURL(url);
});

// Funciones auxiliares
function showLoading(text) {
    loadingText.textContent = text;
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

function showError(message) {
    alert(message);
}

// Cargar métricas al iniciar
window.addEventListener('load', () => {
    loadMetrics();
    loadFeatureImportance();
});
