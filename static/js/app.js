/**
 * Simple Subtitle Generator - Web Interface
 * ========================================
 * 
 * Simplified JavaScript for basic subtitle generation functionality only.
 * Features:
 * - File upload with drag & drop
 * - Form validation
 * - Progress tracking
 * - Loading overlay
 * - File clear functionality
 */

class SimpleSubtitleApp {
    constructor() {
        console.log('SimpleSubtitleApp: Initializing...');
        this.init();
    }

    init() {
        console.log('SimpleSubtitleApp: Starting initialization...');
        this.setupEventListeners();
        this.initFileUpload();
        console.log('SimpleSubtitleApp: Initialization complete.');
    }

    setupEventListeners() {
        console.log('SimpleSubtitleApp: Setting up event listeners...');
        
        // Form submission
        const form = document.getElementById('subtitleForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleSubmit(e, form));
            console.log('SimpleSubtitleApp: Form submit listener added.');
        }

        // Clear button
        const clearBtn = document.getElementById('clearBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', (e) => this.handleClear(e));
            console.log('SimpleSubtitleApp: Clear button listener added.');
        }

        // Progress updates
        this.setupProgressUpdates();
        
        console.log('SimpleSubtitleApp: All event listeners set up successfully.');
    }

    initFileUpload() {
        console.log('SimpleSubtitleApp: Initializing file upload...');
        
        const fileInput = document.getElementById('fileInput');
        const fileUpload = document.querySelector('.file-upload');

        if (!fileInput || !fileUpload) {
            console.error('SimpleSubtitleApp: File input or upload element not found.');
            return;
        }

        // File input change
        fileInput.addEventListener('change', (e) => this.handleFileSelect(e, fileUpload));

        // Drag and drop
        fileUpload.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUpload.classList.add('drag-over');
        });

        fileUpload.addEventListener('dragleave', () => {
            fileUpload.classList.remove('drag-over');
        });

        fileUpload.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUpload.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                this.handleFileSelect({ target: { files: files } }, fileUpload);
            }
        });

        // Click to browse
        fileUpload.addEventListener('click', () => {
            fileInput.click();
        });

        console.log('SimpleSubtitleApp: File upload initialized successfully.');
    }

    handleFileSelect(e, fileUploadElement) {
        console.log('SimpleSubtitleApp: File(s) selected.');
        const files = e.target.files;
        if (files.length > 0) {
            const file = files[0];
            console.log(`SimpleSubtitleApp: Selected file: ${file.name}, type: ${file.type}, size: ${file.size}`);
            this.updateFileUploadUI(file, fileUploadElement);
            this.validateFile(file, fileUploadElement);
        } else {
            console.warn('SimpleSubtitleApp: No files selected.');
        }
    }

    updateFileUploadUI(file, fileUploadElement) {
        console.log(`SimpleSubtitleApp: Updating UI for file ${file.name}.`);
        const fileUploadText = fileUploadElement.querySelector('.file-upload-text');
        const fileUploadHint = fileUploadElement.querySelector('.file-upload-hint');
        
        if (fileUploadText && fileUploadHint) {
            fileUploadText.textContent = file.name;
            fileUploadHint.textContent = `${this.formatFileSize(file.size)} • ${file.type || 'Unknown type'}`;
            fileUploadElement.classList.add('file-selected');
            console.log(`SimpleSubtitleApp: UI updated for ${file.name}.`);
        } else {
            console.error('SimpleSubtitleApp: Could not find fileUploadText or fileUploadHint.', {fileUploadElement});
        }
    }

    validateFile(file, fileUploadElement) {
        console.log(`SimpleSubtitleApp: Validating file ${file.name}.`);
        const allowedTypes = [
            'video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/webm',
            'audio/mp3', 'audio/wav', 'audio/m4a', 'audio/flac', 'audio/aac'
        ];
        
        const maxSize = 500 * 1024 * 1024; // 500MB
        
        if (file.size > maxSize) {
            this.showMessage('Dosya çok büyük. Maksimum boyut 500MB.', 'error');
            this.resetFileUploadUI(fileUploadElement);
            console.error(`SimpleSubtitleApp: File ${file.name} is too large (${this.formatFileSize(file.size)}).`);
            return false;
        }
        
        // Basic type check (more flexible for various formats)
        const isValidType = allowedTypes.some(type => 
            file.type.includes(type.split('/')[1]) || 
            file.name.toLowerCase().includes(type.split('/')[1])
        );
        
        if (!isValidType) {
            this.showMessage('Desteklenmeyen dosya türü. Lütfen bir video veya ses dosyası seçin.', 'error');
            this.resetFileUploadUI(fileUploadElement);
            console.error(`SimpleSubtitleApp: File ${file.name} has unsupported type (${file.type}).`);
            return false;
        }
        
        console.log(`SimpleSubtitleApp: File ${file.name} is valid.`);
        return true;
    }

    resetFileUploadUI(fileUploadElement) {
        console.log('SimpleSubtitleApp: Resetting file upload UI.');
        const fileUploadText = fileUploadElement.querySelector('.file-upload-text');
        const fileUploadHint = fileUploadElement.querySelector('.file-upload-hint');
        if (fileUploadText) fileUploadText.textContent = 'Dosyanızı buraya sürükleyin veya göz atmak için tıklayın';
        if (fileUploadHint) fileUploadHint.textContent = 'MP4, AVI, MOV, MKV, MP3, WAV, M4A ve daha fazlasını destekler';
        fileUploadElement.classList.remove('file-selected');
        console.log('SimpleSubtitleApp: File upload UI reset complete.');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bayt';
        const k = 1024;
        const sizes = ['Bayt', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async handleSubmit(e, formElement) {
        e.preventDefault();
        console.log(`SimpleSubtitleApp: Form submission initiated for form ID: ${formElement.id || 'unknown'}.`);
        
        const fileInput = formElement.querySelector('input[type="file"]');
        const fileUploadElement = formElement.querySelector('.file-upload');

        if (!fileInput || !this.validateForm(fileInput, fileUploadElement)) {
            console.warn(`SimpleSubtitleApp: Form validation failed for form ID: ${formElement.id || 'unknown'}.`);
            return;
        }

        this.showLoading();
        
        try {
            const formData = new FormData(formElement);
            console.log('SimpleSubtitleApp: FormData created.');
            
            // Simulate progress updates
            this.updateProgress(10, 'Dosya yükleniyor...');
            console.log('SimpleSubtitleApp: Sending fetch request to /upload.');
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            console.log(`SimpleSubtitleApp: Received response from /upload. Status: ${response.status}.`);
            this.updateProgress(50, 'Ses işleniyor...');
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error(`SimpleSubtitleApp: HTTP error! Status: ${response.status}, Response: ${errorText}`);
                throw new Error(`HTTP hatası! Durum: ${response.status}, Detay: ${errorText.substring(0, 200)}...`);
            }

            this.updateProgress(80, 'Altyazılar oluşturuluyor...');
            console.log('SimpleSubtitleApp: Processing complete, handling response.');
            
            // Handle response
            const result = await response.text();
            
            this.updateProgress(100, 'Tamamlandı!');
            
            setTimeout(() => {
                this.hideLoading();
                
                // Check if response is a redirect or contains success message
                if (result.includes('success') || response.redirected) {
                    this.showMessage('Altyazılar başarıyla oluşturuldu!', 'success');
                    console.log('SimpleSubtitleApp: Success message displayed, reloading page.');
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                } else {
                    // Parse and display any error messages
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(result, 'text/html');
                    const errorMsg = doc.querySelector('.message-error');
                    
                    if (errorMsg) {
                        this.showMessage(errorMsg.textContent, 'error');
                        console.error('SimpleSubtitleApp: Error message from server:', errorMsg.textContent);
                    } else {
                        this.showMessage('İşlem tamamlandı. Çıktı dosyalarını kontrol edin.', 'success');
                        console.log('SimpleSubtitleApp: Unknown successful completion, reloading page.');
                        setTimeout(() => {
                            window.location.reload();
                        }, 1500);
                    }
                }
            }, 1000);
            
        } catch (error) {
            console.error('SimpleSubtitleApp: Hata oluştu:', error);
            this.hideLoading();
            this.showMessage(`Hata: ${error.message}`, 'error');
        }
    }

    validateForm(fileInput, fileUploadElement) {
        console.log('SimpleSubtitleApp: Validating form.');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showMessage('Lütfen işlenecek bir dosya seçin.', 'error');
            console.warn('SimpleSubtitleApp: No file selected.');
            return false;
        }
        
        return this.validateFile(file, fileUploadElement);
    }

    handleClear(e) {
        e.preventDefault();
        console.log('SimpleSubtitleApp: Clear files requested.');
        
        if (confirm('Tüm yüklenen ve oluşturulan dosyalar silinecek. Devam etmek istiyor musunuz?')) {
            console.log('SimpleSubtitleApp: User confirmed file clearing.');
            window.location.href = '/clear';
        } else {
            console.log('SimpleSubtitleApp: User cancelled file clearing.');
        }
    }

    setupProgressUpdates() {
        // Auto-refresh for progress updates (simple polling)
        setInterval(() => {
            const loadingOverlay = document.getElementById('loadingOverlay');
            if (loadingOverlay && loadingOverlay.style.display !== 'none') {
                // Check for new files or updates
                this.checkForUpdates();
            }
        }, 3000);
    }

    async checkForUpdates() {
        try {
            // Simple check - just reload if processing is likely done
            const response = await fetch('/');
            if (response.ok) {
                const text = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(text, 'text/html');
                const newFiles = doc.querySelectorAll('.file-item');
                const currentFiles = document.querySelectorAll('.file-item');
                
                if (newFiles.length !== currentFiles.length) {
                    console.log('SimpleSubtitleApp: New files detected, reloading page.');
                    window.location.reload();
                }
            }
        } catch (error) {
            console.log('SimpleSubtitleApp: Update check failed:', error);
        }
    }

    showLoading() {
        console.log('SimpleSubtitleApp: Showing loading overlay.');
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = 'flex';
        }
    }

    hideLoading() {
        console.log('SimpleSubtitleApp: Hiding loading overlay.');
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }

    updateProgress(percentage, message) {
        console.log(`SimpleSubtitleApp: Progress update: ${percentage}% - ${message}`);
        
        const progressFill = document.querySelector('.progress-fill');
        const loadingText = document.querySelector('.loading-text');
        const loadingSubtext = document.querySelector('.loading-subtext');
        
        if (progressFill) {
            progressFill.style.width = `${percentage}%`;
        }
        
        if (loadingText) {
            loadingText.textContent = message;
        }
        
        if (loadingSubtext) {
            loadingSubtext.textContent = `${percentage}% tamamlandı`;
        }
    }

    showMessage(text, type = 'info') {
        console.log(`SimpleSubtitleApp: Showing message: ${type} - ${text}`);
        
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());
        
        // Create new message
        const message = document.createElement('div');
        message.className = `message message-${type} fade-in-up`;
        message.innerHTML = `
            <span>${type === 'success' ? '✓' : '✗'}</span>
            ${text}
        `;
        
        // Insert after header
        const header = document.querySelector('.header');
        if (header && header.nextSibling) {
            header.parentNode.insertBefore(message, header.nextSibling);
        } else {
            document.querySelector('.container').prepend(message);
        }
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (message.parentNode) {
                message.remove();
            }
        }, 5000);
    }
}

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('SimpleSubtitleApp: DOM ready, initializing application...');
    new SimpleSubtitleApp();
});

console.log('SimpleSubtitleApp: Script loaded successfully.');