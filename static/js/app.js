// Professional Subtitle Tool - Frontend JavaScript
class SubtitleTool {
    constructor() {
        console.log('SubtitleTool: Constructor called.');
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
        console.log('SubtitleTool: Initializing form elements.');
        // Initialize form elements for basic subtitles
        this.basicForm = document.getElementById('subtitleForm');
        this.basicFileInput = document.getElementById('fileInput');
        this.basicFileUpload = this.basicForm.querySelector('.file-upload');
        this.submitBtn = document.getElementById('submitBtn');

        // Initialize form elements for multilingual TTS
        this.multilingualForm = document.getElementById('multilingualForm');
        this.multilingualFileInput = document.getElementById('multilingualFileInput');
        this.multilingualFileUpload = this.multilingualForm.querySelector('.file-upload');

        // Initialize form elements for record audio
        this.recordAudioForm = document.getElementById('recordAudioForm');
        this.recordVideoInput = document.getElementById('recordVideoInput');
        this.recordVideoFileUpload = this.recordAudioForm.querySelector('.file-upload');
        
        // Initialize drag and drop for all file upload areas
        console.log('SubtitleTool: Initializing drag and drop for basic form.');
        this.initDragAndDrop(this.basicFileUpload, this.basicFileInput);
        console.log('SubtitleTool: Initializing drag and drop for multilingual form.');
        this.initDragAndDrop(this.multilingualFileUpload, this.multilingualFileInput);
        console.log('SubtitleTool: Initializing drag and drop for record audio form.');
        this.initDragAndDrop(this.recordVideoFileUpload, this.recordVideoInput);
        
        // Initialize style preview
        this.initStylePreview();
        
        // Load saved settings
        this.loadSettings();
        console.log('SubtitleTool: Initialization complete.');
    }

    bindEvents() {
        console.log('SubtitleTool: Binding events.');
        // Basic Subtitles Form submission
        if (this.basicForm) {
            console.log('SubtitleTool: Binding submit event for basicForm.');
            this.basicForm.addEventListener('submit', (e) => this.handleSubmit(e, this.basicForm));
        }

        // Basic File input change
        if (this.basicFileInput) {
            console.log('SubtitleTool: Binding change event for basicFileInput.');
            this.basicFileInput.addEventListener('change', (e) => this.handleFileSelect(e, this.basicFileUpload));
        }

        // Style change
        const styleSelect = document.getElementById('style');
        if (styleSelect) {
            console.log('SubtitleTool: Binding change event for styleSelect.');
            styleSelect.addEventListener('change', (e) => this.updateStylePreview(e.target.value));
        }

        // Save settings on change for basic form
        const basicFormInputs = this.basicForm?.querySelectorAll('input, select');
        basicFormInputs?.forEach(input => {
            input.addEventListener('change', () => this.saveSettings(this.basicForm));
        });

        // Clear files button
        const clearBtn = document.getElementById('clearBtn');
        if (clearBtn) {
            console.log('SubtitleTool: Binding click event for clearBtn.');
            clearBtn.addEventListener('click', (e) => this.handleClearFiles(e));
        }
        
        // Multilingual form submission
        if (this.multilingualForm) {
            console.log('SubtitleTool: Binding submit event for multilingualForm.');
            this.multilingualForm.addEventListener('submit', (e) => this.handleMultilingualSubmit(e));
        }

        // Multilingual file input change
        if (this.multilingualFileInput) {
            console.log('SubtitleTool: Binding change event for multilingualFileInput.');
            this.multilingualFileInput.addEventListener('change', (e) => this.handleFileSelect(e, this.multilingualFileUpload));
        }

        // Record Audio form submission
        if (this.recordAudioForm) {
            console.log('SubtitleTool: Binding submit event for recordAudioForm.');
            this.recordAudioForm.addEventListener('submit', (e) => this.handleRecordAndProcess(e));
        }

        // Record Video input change
        if (this.recordVideoInput) {
            console.log('SubtitleTool: Binding change event for recordVideoInput.');
            this.recordVideoInput.addEventListener('change', (e) => this.handleFileSelect(e, this.recordVideoFileUpload));
        }
        
        // Audio mix range slider
        const audioMixRange = document.getElementById('original_audio_mix');
        if (audioMixRange) {
            console.log('SubtitleTool: Binding input event for audioMixRange.');
            audioMixRange.addEventListener('input', (e) => {
                const value = Math.round(e.target.value * 100);
                document.getElementById('audioMixValue').textContent = `${value}%`;
            });
        }
        console.log('SubtitleTool: Events binding complete.');
    }

    initDragAndDrop(fileUploadElement, fileInputElement) {
        if (!fileUploadElement) {
            console.warn('initDragAndDrop: fileUploadElement is null.');
            return;
        }
        console.log(`initDragAndDrop: Initializing for ${fileInputElement.id || 'unknown'} file input.`);

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            fileUploadElement.addEventListener(eventName, this.preventDefaults, false);
            console.log(`initDragAndDrop: Added ${eventName} listener for ${fileInputElement.id || 'unknown'}.`);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            fileUploadElement.addEventListener(eventName, () => {
                fileUploadElement.classList.add('drag-over');
                console.log(`initDragAndDrop: ${eventName} - Added drag-over class for ${fileInputElement.id || 'unknown'}.`);
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            fileUploadElement.addEventListener(eventName, () => {
                fileUploadElement.classList.remove('drag-over');
                console.log(`initDragAndDrop: ${eventName} - Removed drag-over class for ${fileInputElement.id || 'unknown'}.`);
            }, false);
        });

        fileUploadElement.addEventListener('drop', (e) => this.handleDrop(e, fileInputElement, fileUploadElement), false);
        console.log(`initDragAndDrop: Added drop listener for ${fileInputElement.id || 'unknown'}.`);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
        // console.log(`preventDefaults: ${e.type} event prevented.`);
    }

    handleDrop(e, fileInputElement, fileUploadElement) {
        console.log('handleDrop: File dropped.');
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            console.log(`handleDrop: Found ${files.length} files. First file: ${files[0].name}`);
            fileInputElement.files = files;
            this.handleFileSelect({ target: { files } }, fileUploadElement);
        } else {
            console.warn('handleDrop: No files found in drop event.');
        }
    }

    handleFileSelect(e, fileUploadElement) {
        console.log('handleFileSelect: File(s) selected.');
        const files = e.target.files;
        if (files.length > 0) {
            const file = files[0];
            console.log(`handleFileSelect: Selected file: ${file.name}, type: ${file.type}, size: ${file.size}`);
            this.updateFileUploadUI(file, fileUploadElement);
            this.validateFile(file, fileUploadElement);
        } else {
            console.warn('handleFileSelect: No files selected.');
        }
    }

    updateFileUploadUI(file, fileUploadElement) {
        console.log(`updateFileUploadUI: Updating UI for file ${file.name}.`);
        const fileUploadText = fileUploadElement.querySelector('.file-upload-text');
        const fileUploadHint = fileUploadElement.querySelector('.file-upload-hint');
        
        if (fileUploadText && fileUploadHint) {
            fileUploadText.textContent = file.name;
            fileUploadHint.textContent = `${this.formatFileSize(file.size)} • ${file.type || 'Unknown type'}`;
            fileUploadElement.classList.add('file-selected');
            console.log(`updateFileUploadUI: UI updated for ${file.name}.`);
        } else {
            console.error('updateFileUploadUI: Could not find fileUploadText or fileUploadHint.', {fileUploadElement});
        }
    }

    validateFile(file, fileUploadElement) {
        console.log(`validateFile: Validating file ${file.name}.`);
        const allowedTypes = [
            'video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/webm',
            'audio/mp3', 'audio/wav', 'audio/m4a', 'audio/flac', 'audio/aac'
        ];
        
        const maxSize = 500 * 1024 * 1024; // 500MB
        
        if (file.size > maxSize) {
            this.showMessage('Dosya çok büyük. Maksimum boyut 500MB.', 'error');
            this.resetFileUploadUI(fileUploadElement); // Reset the UI on error
            console.error(`validateFile: File ${file.name} is too large (${this.formatFileSize(file.size)}).`);
            return false;
        }
        
        // Basic type check (more flexible for various formats)
        const isValidType = allowedTypes.some(type => 
            file.type.includes(type.split('/')[1]) || 
            file.name.toLowerCase().includes(type.split('/')[1])
        );
        
        if (!isValidType) {
            this.showMessage('Desteklenmeyen dosya türü. Lütfen bir video veya ses dosyası seçin.', 'error');
            this.resetFileUploadUI(fileUploadElement); // Reset the UI on error
            console.error(`validateFile: File ${file.name} has unsupported type (${file.type}).`);
            return false;
        }
        
        console.log(`validateFile: File ${file.name} is valid.`);
        return true;
    }

    resetFileUploadUI(fileUploadElement) {
        console.log('resetFileUploadUI: Resetting UI.', {fileUploadElement});
        const fileUploadText = fileUploadElement.querySelector('.file-upload-text');
        const fileUploadHint = fileUploadElement.querySelector('.file-upload-hint');
        if (fileUploadText) fileUploadText.textContent = 'Dosyanızı buraya sürükleyin veya göz atmak için tıklayın';
        if (fileUploadHint) fileUploadHint.textContent = 'MP4, AVI, MOV, MKV, MP3, WAV, M4A ve daha fazlasını destekler'; // Generic hint
        fileUploadElement.classList.remove('file-selected');
        console.log('resetFileUploadUI: UI reset complete.');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bayt';
        const k = 1024;
        const sizes = ['Bayt', 'KB', 'MB', 'GB'];
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

    async handleSubmit(e, formElement) {
        e.preventDefault();
        console.log(`handleSubmit: Form submission initiated for form ID: ${formElement.id || 'unknown'}.`);
        
        const fileInput = formElement.querySelector('input[type="file"]');
        const fileUploadElement = formElement.querySelector('.file-upload');

        if (!fileInput || !this.validateForm(fileInput, fileUploadElement)) {
            console.warn(`handleSubmit: Form validation failed for form ID: ${formElement.id || 'unknown'}.`);
            return;
        }

        this.showLoading();
        
        try {
            const formData = new FormData(formElement);
            console.log('handleSubmit: FormData created.');
            
            // Simulate progress updates
            this.updateProgress(10, 'Dosya yükleniyor...');
            console.log('handleSubmit: Sending fetch request to /upload.');
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            console.log(`handleSubmit: Received response from /upload. Status: ${response.status}.`);
            this.updateProgress(50, 'Ses işleniyor...');
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error(`handleSubmit: HTTP error! Status: ${response.status}, Response: ${errorText}`);
                throw new Error(`HTTP hatası! Durum: ${response.status}, Detay: ${errorText.substring(0, 200)}...`);
            }

            this.updateProgress(80, 'Altyazılar oluşturuluyor...');
            console.log('handleSubmit: Processing complete, handling response.');
            
            // Handle response
            const result = await response.text();
            
            this.updateProgress(100, 'Tamamlandı!');
            
            setTimeout(() => {
                this.hideLoading();
                
                // Check if response is a redirect or contains success message
                if (result.includes('success') || response.redirected) {
                    this.showMessage('Altyazılar başarıyla oluşturuldu!', 'success');
                    console.log('handleSubmit: Success message displayed, reloading page.');
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
                        console.error('handleSubmit: Error message from server:', errorMsg.textContent);
                    } else {
                        this.showMessage('İşlem tamamlandı. Çıktı dosyalarını kontrol edin.', 'success');
                        console.log('handleSubmit: Unknown successful completion, reloading page.');
                        setTimeout(() => {
                            window.location.reload();
                        }, 1500);
                    }
                }
            }, 1000);
            
        } catch (error) {
            console.error('handleSubmit: Hata oluştu:', error);
            this.hideLoading();
            this.showMessage(`Hata: ${error.message}`, 'error');
        }
    }

    validateForm(fileInput, fileUploadElement) {
        console.log('validateForm: Validating form.');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showMessage('Lütfen işlenecek bir dosya seçin.', 'error');
            console.warn('validateForm: No file selected.');
            return false;
        }
        
        return this.validateFile(file, fileUploadElement);
    }
    
    async handleMultilingualSubmit(e) {
        e.preventDefault();
        console.log('handleMultilingualSubmit: Multilingual form submission initiated.');
        
        if (!this.validateMultilingualForm()) {
            console.warn('handleMultilingualSubmit: Multilingual form validation failed.');
            return;
        }

        this.showLoading('Çok Dilli TTS İşleniyor');
        
        try {
            const formData = new FormData(this.multilingualForm);
            console.log('handleMultilingualSubmit: FormData created.');
            
            // Update progress for multilingual processing
            this.updateProgress(5, 'Video dosyası yükleniyor...');
            console.log('handleMultilingualSubmit: Sending fetch request to /upload (multilingual).');
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            console.log(`handleMultilingualSubmit: Received response from /upload. Status: ${response.status}.`);
            this.updateProgress(20, 'Altyazılar oluşturuluyor...');
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error(`handleMultilingualSubmit: HTTP error! Status: ${response.status}, Response: ${errorText}`);
                throw new Error(`HTTP hatası! Durum: ${response.status}, Detay: ${errorText.substring(0, 200)}...`);
            }

            this.updateProgress(40, 'Seçilen diller için TTS işleniyor...');
            console.log('handleMultilingualSubmit: Processing TTS.');
            
            // Handle response
            const result = await response.text();
            
            this.updateProgress(80, 'Ses ve video birleştiriliyor...');
            
            setTimeout(() => {
                this.updateProgress(100, 'Tamamlandı!');
                
                setTimeout(() => {
                    this.hideLoading();
                    
                    // Check if response contains success message
                    if (result.includes('success') || response.redirected) {
                        this.showMessage('Çok dilli TTS videoları başarıyla oluşturuldu!', 'success');
                        console.log('handleMultilingualSubmit: Success message displayed, reloading page.');
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
                            console.error('handleMultilingualSubmit: Error message from server:', errorMsg.textContent);
                        } else {
                            this.showMessage('Çok dilli işlem tamamlandı. Çıktı dosyalarını kontrol edin.', 'success');
                            console.log('handleMultilingualSubmit: Unknown successful completion, reloading page.');
                            setTimeout(() => {
                                window.location.reload();
                            }, 2000);
                        }
                    }
                }, 1000);
            }, 2000);
            
        } catch (error) {
            console.error('handleMultilingualSubmit: Hata oluştu:', error);
            this.hideLoading();
            this.showMessage(`Hata: ${error.message}`, 'error');
        }
    }
    
    validateMultilingualForm() {
        console.log('validateMultilingualForm: Validating multilingual form.');
        const file = this.multilingualFileInput.files[0];
        
        if (!file) {
            this.showMessage('Lütfen işlenecek bir video dosyası seçin.', 'error');
            console.warn('validateMultilingualForm: No video file selected.');
            return false;
        }
        
        // Check if at least one language is selected
        const selectedLanguages = this.multilingualForm.querySelectorAll('input[name="tts_languages"]:checked');
        if (selectedLanguages.length === 0) {
            this.showMessage('Lütfen TTS oluşturma için en az bir dil seçin.', 'error');
            console.warn('validateMultilingualForm: No TTS language selected.');
            return false;
        }
        
        return this.validateFile(file, this.multilingualFileUpload);
    }

    showLoading(title = 'Dosyanız işleniyor...') {
        console.log(`showLoading: Displaying loading overlay with title: "${title}".`);
        if (this.loadingOverlay) {
            this.loadingOverlay.classList.add('active');
            this.updateProgress(0, 'Başlatılıyor...');
            
            if (this.loadingText) {
                this.loadingText.textContent = title;
            }
        }
        
        if (this.submitBtn) {
            this.submitBtn.disabled = true;
            console.log('showLoading: Basic submit button disabled.');
        }
        
        if (this.multilingualSubmitBtn) {
            this.multilingualSubmitBtn.disabled = true;
            console.log('showLoading: Multilingual submit button disabled.');
        }
        
        // Disable recordAudioForm submit button as well
        if (this.recordAudioForm) {
            this.recordAudioForm.querySelector('button[type="submit"]').disabled = true;
            console.log('showLoading: Record audio submit button disabled.');
        }
    }

    hideLoading() {
        console.log('hideLoading: Hiding loading overlay.');
        if (this.loadingOverlay) {
            this.loadingOverlay.classList.remove('active');
        }
        
        if (this.submitBtn) {
            this.submitBtn.disabled = false;
            console.log('hideLoading: Basic submit button enabled.');
        }
        
        if (this.multilingualSubmitBtn) {
            this.multilingualSubmitBtn.disabled = false;
            console.log('hideLoading: Multilingual submit button enabled.');
        }
        
        // Re-enable recordAudioForm submit button (if audio is ready)
        if (this.recordAudioForm) {
            const submitButton = this.recordAudioForm.querySelector('button[type="submit"]');
            if (submitButton && this.audioPlayback && this.audioPlayback.src !== '') {
                submitButton.disabled = false;
                console.log('hideLoading: Record audio submit button enabled (audio ready).');
            } else if (submitButton) {
                // Ensure it's disabled if no audio is ready yet
                submitButton.disabled = true;
                console.log('hideLoading: Record audio submit button disabled (no audio ready).');
            }
        }
    }

    updateProgress(percentage, text) {
        console.log(`updateProgress: Progress updated to ${percentage}% with text: "${text}".`);
        if (this.progressBar) {
            this.progressBar.style.width = `${percentage}%`;
        }
        
        if (this.loadingText) {
            this.loadingText.textContent = text;
        }
        
        if (this.loadingSubtext) {
            this.loadingSubtext.textContent = `${percentage}% tamamlandı`;
        }
    }

    showMessage(message, type = 'info') {
        console.log(`showMessage: Displaying message: "${message}" (Type: ${type}).`);
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
                console.log('showMessage: Message removed after 5 seconds.');
            }, 5000);
        }
    }

    async handleClearFiles(e) {
        e.preventDefault();
        console.log('handleClearFiles: Clear files button clicked.');
        
        if (!confirm('Yüklenen ve çıktı dosyalarının tümünü temizlemek istediğinizden emin misiniz?')) {
            console.log('handleClearFiles: Clear files action cancelled by user.');
            return;
        }
        console.log('handleClearFiles: Clear files action confirmed.');
        
        try {
            console.log('handleClearFiles: Sending fetch request to /clear.');
            const response = await fetch('/clear', {
                method: 'GET'
            });
            
            if (response.ok) {
                this.showMessage('Dosyalar başarıyla temizlendi!', 'success');
                console.log('handleClearFiles: Files cleared successfully, reloading page.');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                const errorText = await response.text();
                console.error(`handleClearFiles: Failed to clear files. Status: ${response.status}, Response: ${errorText}`);
                throw new Error(`Dosyalar temizlenemedi. Detay: ${errorText.substring(0, 200)}...`);
            }
        } catch (error) {
            console.error('handleClearFiles: Hata oluştu:', error);
            this.showMessage(`Dosyalar temizlenirken hata oluştu: ${error.message}`, 'error');
        }
    }

    saveSettings(formElement) {
        console.log(`saveSettings: Saving settings for form ID: ${formElement.id || 'unknown'}.`);
        const settings = {};
        const formInputs = formElement?.querySelectorAll('input, select');
        
        formInputs?.forEach(input => {
            if (input.type === 'checkbox') {
                settings[input.name] = input.checked;
            } else if (input.type !== 'file') {
                settings[input.name] = input.value;
            }
        });
        
        // Use form ID as part of the key to save settings per form
        if (formElement && formElement.id) {
            localStorage.setItem(`subtitleToolSettings_${formElement.id}`, JSON.stringify(settings));
            console.log(`saveSettings: Settings saved for ${formElement.id || 'unknown'}.`);
        } else {
            console.warn('saveSettings: Form element or ID not found, settings not saved.', {formElement});
        }
    }

    loadSettings() {
        console.log('loadSettings: Loading settings for basic form.');
        // Load settings for basic form
        try {
            const settings = JSON.parse(localStorage.getItem('subtitleToolSettings_subtitleForm') || '{}');
            
            Object.keys(settings).forEach(key => {
                const input = this.basicForm?.querySelector(`[name="${key}"]`);
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
            console.log('loadSettings: Settings loaded for basic form.');
        } catch (error) {
            console.warn('loadSettings: Could not load saved settings for basic form:', error);
        }
        // Note: Currently not loading settings for multilingual or record_audio forms
        // as their state management is less critical or tied to current session.
    }

    // New method for handling audio recording
    initAudioRecording() {
        console.log('initAudioRecording: Initializing audio recording features.');
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.mediaStream = null;

        // Get elements after DOM is loaded
        this.startRecordingBtn = document.getElementById('startRecordingBtn');
        this.stopRecordingBtn = document.getElementById('stopRecordingBtn');
        this.saveRecordingBtn = document.getElementById('saveRecordingBtn');
        this.recordingStatus = document.getElementById('recordingStatus');
        this.audioPlayback = document.getElementById('audioPlayback');
        this.recordVideoInput = document.getElementById('recordVideoInput');
        this.recordAudioForm = document.getElementById('recordAudioForm');
        this.videoPlayback = document.getElementById('videoPlayback'); // New video element
        this.videoPlaybackContainer = document.querySelector('.video-playback-container'); // New container

        // Also need to get the file upload div for the record video input
        this.recordVideoFileUpload = this.recordAudioForm.querySelector('.file-upload');
        
        // Re-initialize drag and drop for the record video upload area
        console.log('initAudioRecording: Re-initializing drag and drop for record video upload.');
        this.initDragAndDrop(this.recordVideoFileUpload, this.recordVideoInput);

        if (this.startRecordingBtn) {
            console.log('initAudioRecording: Binding click event for startRecordingBtn.');
            this.startRecordingBtn.addEventListener('click', () => this.startRecording());
        }
        if (this.stopRecordingBtn) {
            console.log('initAudioRecording: Binding click event for stopRecordingBtn.');
            this.stopRecordingBtn.addEventListener('click', () => this.stopRecording());
        }
        if (this.saveRecordingBtn) {
            console.log('initAudioRecording: Binding click event for saveRecordingBtn.');
            this.saveRecordingBtn.addEventListener('click', () => this.saveRecording());
        }
        if (this.recordAudioForm) {
            console.log('initAudioRecording: Binding submit event for recordAudioForm.');
            this.recordAudioForm.addEventListener('submit', (e) => this.handleRecordAndProcess(e));
        }

        // Handle video file selection for recording tab
        if (this.recordVideoInput) {
            console.log('initAudioRecording: Binding change event for recordVideoInput to load video.');
            this.recordVideoInput.addEventListener('change', (e) => this.handleRecordVideoSelect(e));
        }

        // Enable/disable submit button based on recorded audio
        if (this.audioPlayback) {
            console.log('initAudioRecording: Binding play/pause events for audioPlayback.');
            this.audioPlayback.addEventListener('play', () => {
                this.recordAudioForm.querySelector('button[type="submit"]').disabled = false;
                console.log('initAudioRecording: Audio playback started, process button enabled.');
            });
            this.audioPlayback.addEventListener('pause', () => {
                if (this.audioPlayback.src === '') {
                    this.recordAudioForm.querySelector('button[type="submit"]').disabled = true;
                    console.log('initAudioRecording: Audio playback paused and no src, process button disabled.');
                }
            });
        }
        console.log('initAudioRecording: Audio recording initialization complete.');
    }

    handleRecordVideoSelect(e) {
        console.log('handleRecordVideoSelect: Video file selected for recording tab.');
        const files = e.target.files;
        if (files.length > 0) {
            const file = files[0];
            if (this.videoPlaybackContainer) {
                this.videoPlaybackContainer.style.display = 'block';
                this.videoPlayback.src = URL.createObjectURL(file);
                this.videoPlayback.load();
                console.log(`handleRecordVideoSelect: Video loaded: ${file.name}`);
            }
            // Also update the file upload UI for visual feedback
            this.updateFileUploadUI(file, this.recordVideoFileUpload);
            this.validateFile(file, this.recordVideoFileUpload);
        } else {
            if (this.videoPlaybackContainer) {
                this.videoPlaybackContainer.style.display = 'none';
                this.videoPlayback.src = '';
            }
            this.resetFileUploadUI(this.recordVideoFileUpload);
            console.log('handleRecordVideoSelect: No video file selected, video player hidden.');
        }
    }

    async startRecording() {
        console.log('startRecording: Attempting to start recording.');
        try {
            this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(this.mediaStream);
            this.audioChunks = [];
            console.log('startRecording: Microphone access granted, MediaRecorder initialized.');

            this.mediaRecorder.ondataavailable = event => {
                this.audioChunks.push(event.data);
                console.log(`startRecording: Audio data available, chunk size: ${event.data.size}.`);
            };

            this.mediaRecorder.onstop = () => {
                console.log('startRecording: MediaRecorder stopped. Creating audio blob.');
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                const audioUrl = URL.createObjectURL(audioBlob);
                this.audioPlayback.src = audioUrl;
                this.audioPlayback.style.display = 'block';
                this.saveRecordingBtn.disabled = false;
                this.recordAudioForm.querySelector('button[type="submit"]').disabled = false;
                console.log('startRecording: Audio blob created and set for playback. Save/Process buttons enabled.');
            };

            this.mediaRecorder.start();
            this.recordingStatus.textContent = 'Kaydediliyor...';
            this.startRecordingBtn.disabled = true;
            this.stopRecordingBtn.disabled = false;
            this.saveRecordingBtn.disabled = true; // Disable save until stop
            this.recordAudioForm.querySelector('button[type="submit"]').disabled = true; // Disable process until save
            this.showMessage('Ses kaydı başlatıldı!', 'info');
            console.log('startRecording: Recording started. UI updated.');
            
            // Start video playback if a video is loaded
            if (this.videoPlayback && !this.videoPlayback.paused && this.videoPlayback.src) {
                this.videoPlayback.play();
                console.log('startRecording: Video playback started.');
            }

        } catch (err) {
            console.error('startRecording: Mikrofon erişimi reddedildi veya hata oluştu:', err);
            this.showMessage('Mikrofon erişimi reddedildi veya hata oluştu.', 'error');
        }
    }

    stopRecording() {
        console.log('stopRecording: Attempting to stop recording.');
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
            this.mediaStream.getTracks().forEach(track => track.stop());
            this.recordingStatus.textContent = 'Kayıt Durduruldu';
            this.startRecordingBtn.disabled = false;
            this.stopRecordingBtn.disabled = true;
            this.showMessage('Ses kaydı durduruldu.', 'info');
            console.log('stopRecording: Recording stopped. UI updated.');

            // Pause video playback if video is playing
            if (this.videoPlayback && !this.videoPlayback.paused) {
                this.videoPlayback.pause();
                console.log('stopRecording: Video playback paused.');
            }

        } else {
            console.warn('stopRecording: MediaRecorder not active or not in recording state.', {recorderState: this.mediaRecorder?.state});
        }
    }

    async saveRecording() {
        console.log('saveRecording: Save recording button clicked.');
        if (this.audioChunks.length === 0) {
            this.showMessage('Henüz bir kayıt yok.', 'error');
            console.warn('saveRecording: No audio chunks to save.');
            return;
        }
        this.recordingStatus.textContent = 'Kaydedilen ses hazır.';
        this.saveRecordingBtn.disabled = false;
        this.recordAudioForm.querySelector('button[type="submit"]').disabled = false;
        console.log('saveRecording: Audio ready for processing. Process button enabled.');
    }

    async handleRecordAndProcess(e) {
        e.preventDefault();
        console.log('handleRecordAndProcess: Record and Process form submission initiated.');

        if (this.audioChunks.length === 0 && (!this.recordVideoInput || this.recordVideoInput.files.length === 0)) {
            this.showMessage('Lütfen önce ses kaydı yapın veya bir video yükleyin.', 'error');
            console.warn('handleRecordAndProcess: No audio recorded and no video file selected.');
            return;
        }

        this.showLoading('Kaydedilen ses işleniyor...');

        try {
            const formData = new FormData(this.recordAudioForm);
            console.log('handleRecordAndProcess: FormData created.');

            // Append recorded audio blob
            if (this.audioChunks.length > 0) {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                formData.append('audio_file', audioBlob, 'recorded_audio.webm');
                console.log(`handleRecordAndProcess: Appended recorded audio blob, size: ${audioBlob.size}.`);
            }

            // Add video file if selected
            if (this.recordVideoInput && this.recordVideoInput.files.length > 0) {
                const videoFile = this.recordVideoInput.files[0];
                formData.append('video_file', videoFile);
                console.log(`handleRecordAndProcess: Appended video file: ${videoFile.name}, size: ${videoFile.size}.`);
            }

            this.updateProgress(10, 'Ses ve video dosyaları yükleniyor...');
            console.log('handleRecordAndProcess: Sending fetch request to /record_and_process.');

            const response = await fetch('/record_and_process', {
                method: 'POST',
                body: formData
            });

            console.log(`handleRecordAndProcess: Received response from /record_and_process. Status: ${response.status}.`);
            this.updateProgress(50, 'Ses ve video işleniyor, altyazılar oluşturuluyor...');

            const result = await response.text();

            this.updateProgress(100, 'Tamamlandı!');

            setTimeout(() => {
                this.hideLoading();
                if (result.includes('success') || response.redirected) {
                    this.showMessage('Video ve ses başarıyla işlendi, altyazılar oluşturuldu!', 'success');
                    console.log('handleRecordAndProcess: Success message displayed, reloading page.');
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                } else {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(result, 'text/html');
                    const errorMsg = doc.querySelector('.message-error');

                    if (errorMsg) {
                        this.showMessage(errorMsg.textContent, 'error');
                        console.error('handleRecordAndProcess: Error message from server:', errorMsg.textContent);
                    } else {
                        this.showMessage('İşlem tamamlandı. Çıktı dosyalarını kontrol edin.', 'success');
                        console.log('handleRecordAndProcess: Unknown successful completion, reloading page.');
                        setTimeout(() => {
                            window.location.reload();
                        }, 1500);
                    }
                }
            }, 1000);

        } catch (error) {
            console.error('handleRecordAndProcess: Hata oluştu:', error);
            this.hideLoading();
            this.showMessage(`Hata: ${error.message}`, 'error');
        }
    }
}

// Tab switching functionality
function switchTab(tabName, event = null) {
    console.log(`switchTab: Switching to tab: ${tabName}.`);
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab content
    const targetTabMap = {
        'basic': 'basicTab',
        'multilingual': 'multilingualTab',
        'record_audio': 'record_audioTab'
    };
    const targetTabId = targetTabMap[tabName];
    if (targetTabId) {
        document.getElementById(targetTabId).classList.add('active');
        console.log(`switchTab: Activated tab content with ID: ${targetTabId}.`);
    }
    
    // Add active class to clicked button
    let activatedButton = null;
    if (event && event.target && event.target.classList.contains('tab-btn')) {
        activatedButton = event.target;
        console.log(`switchTab: Activated tab button from event.target: ${activatedButton.textContent.trim()}.`);
    } else {
        // Fallback for direct calls or initial load: find the button by tabName
        activatedButton = document.querySelector(`.tab-btn[onclick*="'${tabName}'"]`);
        if (activatedButton) {
            console.log(`switchTab: Fallback: Activated tab button by query selector for tab: ${tabName}.`);
        } else {
            console.warn(`switchTab: Could not find a button for tab: ${tabName}.`);
        }
    }

    if (activatedButton) {
        activatedButton.classList.add('active');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded: Initializing application.');
    const tool = new SubtitleTool();
    tool.initAudioRecording(); // Initialize audio recording features

    // Set initial active tab (e.g., from URL or default to 'basic')
    const urlParams = new URLSearchParams(window.location.search);
    const initialTab = urlParams.get('tab') || 'basic';
    console.log(`DOMContentLoaded: Initial tab set to: ${initialTab}.`);
    switchTab(initialTab);
    console.log('DOMContentLoaded: Application initialized.');
});

// Modal functionality for file previews (on files.html)
document.addEventListener('DOMContentLoaded', () => {
    const previewModal = document.getElementById('previewModal');
    const closeButton = document.querySelector('.modal .close-button');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');

    // Open the modal when an "Önizle" button is clicked
    document.querySelectorAll('.preview-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            const fileUrl = e.target.dataset.fileUrl;
            const fileType = e.target.dataset.fileType;
            const fileName = e.target.closest('.file-item').querySelector('h4').textContent;

            modalTitle.textContent = `${fileName} Önizlemesi`;
            modalBody.innerHTML = '<p>Yükleniyor...</p>';
            previewModal.style.display = 'block';

            try {
                if (fileType === 'video') {
                    modalBody.innerHTML = `<video controls width="100%" src="${fileUrl}" type="video/mp4"></video>`;
                } else if (fileType === 'text') {
                    const response = await fetch(fileUrl);
                    if (!response.ok) {
                        throw new Error(`HTTP hatası! Durum: ${response.status}`);
                    }
                    const textContent = await response.text();
                    modalBody.innerHTML = `<pre class="code-preview">${escapeHtml(textContent)}</pre>`;
                } else {
                    modalBody.innerHTML = '<p>Bu dosya türü için önizleme mevcut değil.</p>';
                }
            } catch (error) {
                console.error('Dosya önizlemesi yüklenirken hata oluştu:', error);
                modalBody.innerHTML = `<p style="color: red;">Önizleme yüklenirken hata oluştu: ${error.message}</p>`;
            }
        });
    });

    // Close the modal when the close button is clicked
    if (closeButton) {
        closeButton.addEventListener('click', () => {
            previewModal.style.display = 'none';
            modalBody.innerHTML = ''; // Clear content when closing
        });
    }

    // Close the modal when clicking outside of it
    window.addEventListener('click', (event) => {
        if (event.target === previewModal) {
            previewModal.style.display = 'none';
            modalBody.innerHTML = ''; // Clear content when closing
        }
    });

    // Helper function to escape HTML for text content
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/\'/g, "&#039;");
    }

    // Handle individual file deletion
    document.querySelectorAll('.delete-file-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            const fileName = e.target.dataset.fileName;
            console.log(`delete-file-btn: Delete button clicked for file: ${fileName}.`);

            if (!confirm(`Are you sure you want to delete the file: ${fileName}?`)) {
                console.log('delete-file-btn: File deletion cancelled by user.');
                return;
            }

            try {
                console.log(`delete-file-btn: Sending delete request for file: ${fileName}.`);
                const response = await fetch(`/delete_file/${fileName}`, {
                    method: 'POST'
                });

                if (response.ok) {
                    alert(`${fileName} başarıyla silindi!`);
                    console.log(`delete-file-btn: File ${fileName} deleted successfully, reloading page.`);
                    window.location.reload();
                } else {
                    const errorText = await response.text();
                    console.error(`delete-file-btn: Failed to delete file ${fileName}. Status: ${response.status}, Response: ${errorText}`);
                    alert(`Dosya silinemedi: ${fileName}. Hata: ${errorText.substring(0, 100)}`);
                }
            } catch (error) {
                console.error(`delete-file-btn: Dosya silinirken hata oluştu: ${fileName}`, error);
                alert(`Dosya silinirken hata oluştu: ${fileName}. Hata: ${error.message}`);
            }
        });
    });
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
        console.log(`SubtitleToolUtils: Downloading file: ${filename} from URL: ${url}.`);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    },
    
    copyToClipboard: async (text) => {
        console.log(`SubtitleToolUtils: Attempting to copy text to clipboard.`);
        try {
            await navigator.clipboard.writeText(text);
            console.log('SubtitleToolUtils: Text copied to clipboard successfully.');
            return true;
        } catch (error) {
            console.error('SubtitleToolUtils: Failed to copy to clipboard:', error);
            return false;
        }
    }
};