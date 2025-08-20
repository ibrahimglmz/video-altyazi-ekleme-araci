// Professional Subtitle Tool - Frontend JavaScript
class SubtitleTool {
    constructor() {
        this.init();
        this.bindEvents();
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.progressBar = document.querySelector('.progress-fill');
        this.loadingText = document.querySelector('.loading-text');
        this.loadingSubtext = document.querySelector('.loading-subtext');
        
        // Initialize multilingual form
        this.multilingualForm = document.getElementById('multilingualForm');
        this.multilingualFileInput = document.getElementById('multilingualFileInput');
        this.multilingualSubmitBtn = document.getElementById('multilingualSubmitBtn');
    }

    init() {
        // Initialize form elements
        this.form = document.getElementById('subtitleForm');
        this.fileInput = document.getElementById('fileInput');
        this.fileUpload = document.querySelector('.file-upload');
        this.submitBtn = document.getElementById('submitBtn');
        
        // Initialize drag and drop
        this.initDragAndDrop();
        
        // Initialize style preview
        this.initStylePreview();
        
        // Load saved settings
        this.loadSettings();
    }

    bindEvents() {
        // Form submission
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        }

        // File input change
        if (this.fileInput) {
            this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }

        // Style change
        const styleSelect = document.getElementById('style');
        if (styleSelect) {
            styleSelect.addEventListener('change', (e) => this.updateStylePreview(e.target.value));
        }

        // Save settings on change
        const formInputs = this.form?.querySelectorAll('input, select');
        formInputs?.forEach(input => {
            input.addEventListener('change', () => this.saveSettings());
        });

        // Clear files button
        const clearBtn = document.getElementById('clearBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', (e) => this.handleClearFiles(e));
        }
        
        // Multilingual form submission
        if (this.multilingualForm) {
            this.multilingualForm.addEventListener('submit', (e) => this.handleMultilingualSubmit(e));
        }

        // Multilingual file input change
        if (this.multilingualFileInput) {
            this.multilingualFileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }
        
        // Audio mix range slider
        const audioMixRange = document.getElementById('original_audio_mix');
        if (audioMixRange) {
            audioMixRange.addEventListener('input', (e) => {
                const value = Math.round(e.target.value * 100);
                document.getElementById('audioMixValue').textContent = `${value}%`;
            });
        }
    }

    initDragAndDrop() {
        if (!this.fileUpload) return;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.fileUpload.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            this.fileUpload.addEventListener(eventName, () => {
                this.fileUpload.classList.add('drag-over');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            this.fileUpload.addEventListener(eventName, () => {
                this.fileUpload.classList.remove('drag-over');
            }, false);
        });

        this.fileUpload.addEventListener('drop', (e) => this.handleDrop(e), false);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            this.fileInput.files = files;
            this.handleFileSelect({ target: { files } });
        }
    }

    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            const file = files[0];
            this.updateFileUploadUI(file);
            this.validateFile(file);
        }
    }

    updateFileUploadUI(file) {
        const fileUploadText = this.fileUpload.querySelector('.file-upload-text');
        const fileUploadHint = this.fileUpload.querySelector('.file-upload-hint');
        
        if (fileUploadText && fileUploadHint) {
            fileUploadText.textContent = file.name;
            fileUploadHint.textContent = `${this.formatFileSize(file.size)} • ${file.type || 'Unknown type'}`;
            this.fileUpload.classList.add('file-selected');
        }
    }

    validateFile(file) {
        const allowedTypes = [
            'video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/webm',
            'audio/mp3', 'audio/wav', 'audio/m4a', 'audio/flac', 'audio/aac'
        ];
        
        const maxSize = 500 * 1024 * 1024; // 500MB
        
        if (file.size > maxSize) {
            this.showMessage('File too large. Maximum size is 500MB.', 'error');
            return false;
        }
        
        // Basic type check (more flexible for various formats)
        const isValidType = allowedTypes.some(type => 
            file.type.includes(type.split('/')[1]) || 
            file.name.toLowerCase().includes(type.split('/')[1])
        );
        
        if (!isValidType) {
            this.showMessage('Unsupported file type. Please select a video or audio file.', 'error');
            return false;
        }
        
        return true;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    initStylePreview() {
        const styleSelect = document.getElementById('style');
        if (styleSelect) {
            this.updateStylePreview(styleSelect.value);
        }
    }

    updateStylePreview(style) {
        const preview = document.querySelector('.style-preview');
        if (!preview) return;

        const styles = {
            default: {
                fontFamily: 'Arial, sans-serif',
                fontSize: '24px',
                color: '#FFFFFF',
                backgroundColor: 'rgba(0, 0, 0, 0.7)',
                textShadow: '2px 2px 4px rgba(0, 0, 0, 0.8)'
            },
            bold: {
                fontFamily: 'Arial, sans-serif',
                fontSize: '28px',
                color: '#FFFFFF',
                backgroundColor: 'rgba(34, 34, 34, 0.85)',
                textShadow: '3px 3px 6px rgba(0, 0, 0, 0.9)',
                fontWeight: 'bold'
            },
            elegant: {
                fontFamily: 'Times New Roman, serif',
                fontSize: '26px',
                color: '#F5F5DC',
                backgroundColor: 'rgba(47, 47, 47, 0.7)',
                textShadow: '1px 1px 2px rgba(0, 0, 0, 0.6)'
            },
            cinema: {
                fontFamily: 'Arial, sans-serif',
                fontSize: '32px',
                color: '#FFD700',
                backgroundColor: 'rgba(0, 0, 0, 0.9)',
                textShadow: '2px 2px 4px rgba(0, 0, 0, 1)'
            },
            modern: {
                fontFamily: 'Roboto, sans-serif',
                fontSize: '24px',
                color: '#00FF41',
                backgroundColor: 'rgba(26, 26, 26, 0.7)',
                textShadow: '1px 1px 2px rgba(0, 0, 0, 0.8)'
            },
            minimal: {
                fontFamily: 'Arial, sans-serif',
                fontSize: '20px',
                color: '#FFFFFF',
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                textShadow: 'none'
            },
            terminal: {
                fontFamily: 'Courier New, monospace',
                fontSize: '22px',
                color: '#00FF00',
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                textShadow: '0 0 5px rgba(0, 255, 0, 0.5)'
            }
        };

        const selectedStyle = styles[style] || styles.default;
        Object.assign(preview.style, selectedStyle);
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            return;
        }

        this.showLoading();
        
        try {
            const formData = new FormData(this.form);
            
            // Simulate progress updates
            this.updateProgress(10, 'Uploading file...');
            
            const response = await fetch('/generate_subtitles', {
                method: 'POST',
                body: formData
            });

            this.updateProgress(50, 'Processing audio...');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            this.updateProgress(80, 'Generating subtitles...');
            
            // Handle response
            const result = await response.text();
            
            this.updateProgress(100, 'Complete!');
            
            setTimeout(() => {
                this.hideLoading();
                
                // Check if response is a redirect or contains success message
                if (result.includes('success') || response.redirected) {
                    this.showMessage('Subtitles generated successfully!', 'success');
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
                    } else {
                        this.showMessage('Processing completed. Check the output files.', 'success');
                        setTimeout(() => {
                            window.location.reload();
                        }, 1500);
                    }
                }
            }, 1000);
            
        } catch (error) {
            console.error('Error:', error);
            this.hideLoading();
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }

    validateForm() {
        const file = this.fileInput.files[0];
        
        if (!file) {
            this.showMessage('Please select a file to process.', 'error');
            return false;
        }
        
        return this.validateFile(file);
    }
    
    async handleMultilingualSubmit(e) {
        e.preventDefault();
        
        if (!this.validateMultilingualForm()) {
            return;
        }

        this.showLoading('Multilingual TTS Processing');
        
        try {
            const formData = new FormData(this.multilingualForm);
            
            // Update progress for multilingual processing
            this.updateProgress(5, 'Uploading video file...');
            
            const response = await fetch('/generate_multilingual_tts', {
                method: 'POST',
                body: formData
            });

            this.updateProgress(20, 'Generating subtitles...');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            this.updateProgress(40, 'Processing TTS for selected languages...');
            
            // Handle response
            const result = await response.text();
            
            this.updateProgress(80, 'Combining audio and video...');
            
            setTimeout(() => {
                this.updateProgress(100, 'Complete!');
                
                setTimeout(() => {
                    this.hideLoading();
                    
                    // Check if response contains success message
                    if (result.includes('success') || response.redirected) {
                        this.showMessage('Multilingual TTS videos generated successfully!', 'success');
                        setTimeout(() => {
                            window.location.reload();
                        }, 2000);
                    } else {
                        // Parse and display any error messages
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(result, 'text/html');
                        const errorMsg = doc.querySelector('.message-error');
                        
                        if (errorMsg) {
                            this.showMessage(errorMsg.textContent, 'error');
                        } else {
                            this.showMessage('Multilingual processing completed. Check the output files.', 'success');
                            setTimeout(() => {
                                window.location.reload();
                            }, 2000);
                        }
                    }
                }, 1000);
            }, 2000);
            
        } catch (error) {
            console.error('Error:', error);
            this.hideLoading();
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    validateMultilingualForm() {
        const file = this.multilingualFileInput.files[0];
        
        if (!file) {
            this.showMessage('Please select a video file to process.', 'error');
            return false;
        }
        
        // Check if at least one language is selected
        const selectedLanguages = this.multilingualForm.querySelectorAll('input[name="tts_languages"]:checked');
        if (selectedLanguages.length === 0) {
            this.showMessage('Please select at least one language for TTS generation.', 'error');
            return false;
        }
        
        return this.validateFile(file);
    }

    showLoading(title = 'Processing your file...') {
        if (this.loadingOverlay) {
            this.loadingOverlay.classList.add('active');
            this.updateProgress(0, 'Initializing...');
            
            if (this.loadingText) {
                this.loadingText.textContent = title;
            }
        }
        
        if (this.submitBtn) {
            this.submitBtn.disabled = true;
        }
        
        if (this.multilingualSubmitBtn) {
            this.multilingualSubmitBtn.disabled = true;
        }
    }

    hideLoading() {
        if (this.loadingOverlay) {
            this.loadingOverlay.classList.remove('active');
        }
        
        if (this.submitBtn) {
            this.submitBtn.disabled = false;
        }
        
        if (this.multilingualSubmitBtn) {
            this.multilingualSubmitBtn.disabled = false;
        }
    }

    updateProgress(percentage, text) {
        if (this.progressBar) {
            this.progressBar.style.width = `${percentage}%`;
        }
        
        if (this.loadingText) {
            this.loadingText.textContent = text;
        }
        
        if (this.loadingSubtext) {
            this.loadingSubtext.textContent = `${percentage}% complete`;
        }
    }

    showMessage(message, type = 'info') {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());
        
        // Create new message
        const messageEl = document.createElement('div');
        messageEl.className = `message message-${type} fade-in-up`;
        
        const icon = type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ';
        messageEl.innerHTML = `<span>${icon}</span> ${message}`;
        
        // Insert at top of form
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(messageEl, container.firstChild);
            
            // Auto remove after 5 seconds
            setTimeout(() => {
                messageEl.remove();
            }, 5000);
        }
    }

    async handleClearFiles(e) {
        e.preventDefault();
        
        if (!confirm('Are you sure you want to clear all uploaded and output files?')) {
            return;
        }
        
        try {
            const response = await fetch('/clear', {
                method: 'GET'
            });
            
            if (response.ok) {
                this.showMessage('Files cleared successfully!', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                throw new Error('Failed to clear files');
            }
        } catch (error) {
            this.showMessage(`Error clearing files: ${error.message}`, 'error');
        }
    }

    saveSettings() {
        const settings = {};
        const formInputs = this.form?.querySelectorAll('input, select');
        
        formInputs?.forEach(input => {
            if (input.type === 'checkbox') {
                settings[input.name] = input.checked;
            } else if (input.type !== 'file') {
                settings[input.name] = input.value;
            }
        });
        
        localStorage.setItem('subtitleToolSettings', JSON.stringify(settings));
    }

    loadSettings() {
        try {
            const settings = JSON.parse(localStorage.getItem('subtitleToolSettings') || '{}');
            
            Object.keys(settings).forEach(key => {
                const input = this.form?.querySelector(`[name="${key}"]`);
                if (input) {
                    if (input.type === 'checkbox') {
                        input.checked = settings[key];
                    } else if (input.type !== 'file') {
                        input.value = settings[key];
                    }
                }
            });
            
            // Update style preview if style was loaded
            if (settings.style) {
                this.updateStylePreview(settings.style);
            }
        } catch (error) {
            console.warn('Could not load saved settings:', error);
        }
    }
}

// Tab switching functionality
function switchTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab content
    const targetTab = tabName === 'basic' ? 'basicTab' : 'multilingualTab';
    document.getElementById(targetTab).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SubtitleTool();
});

// Add some utility functions
window.SubtitleToolUtils = {
    formatTime: (seconds) => {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    
    downloadFile: (url, filename) => {
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    },
    
    copyToClipboard: async (text) => {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (error) {
            console.error('Failed to copy to clipboard:', error);
            return false;
        }
    }
};