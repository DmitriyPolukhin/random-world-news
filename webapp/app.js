/**
 * Random World News - Telegram Mini App
 * Main Application Logic
 */

// ============================================
// Configuration
// ============================================
const CONFIG = {
    // Backend API URL - always use localhost for development
    // When deployed, change this to your production URL
    API_URL: (window.location.protocol === 'file:' || window.location.hostname === 'localhost')
        ? 'http://localhost:8000'
        : window.location.origin,

    // LocalStorage keys
    STORAGE_KEYS: {
        NEWS_COUNT: 'rwn_news_count',
        COUNTRIES_VISITED: 'rwn_countries'
    }
};

// ============================================
// State Management
// ============================================
const state = {
    isLoading: false,
    newsCount: 0,
    countriesVisited: new Set(),
    currentNews: null
};

// ============================================
// DOM Elements
// ============================================
const elements = {
    fetchBtn: document.getElementById('fetch-btn'),
    newsCount: document.getElementById('news-count'),
    headerTitle: document.getElementById('header-title'),

    welcomeState: document.getElementById('welcome-state'),
    loadingState: document.getElementById('loading-state'),
    newsCard: document.getElementById('news-card'),

    newsImageContainer: document.getElementById('news-image-container'),
    newsImage: document.getElementById('news-image'),
    newsTitle: document.getElementById('news-title'),
    newsDescription: document.getElementById('news-description'),
    newsSource: document.getElementById('news-source'),
    newsLanguage: document.getElementById('news-language'),

    readMoreBtn: document.getElementById('read-more-btn'),
    shareBtn: document.getElementById('share-btn')
};

// ============================================
// Telegram Web App Integration
// ============================================
const tg = window.Telegram?.WebApp;

function initTelegram() {
    if (!tg) {
        console.log('Running outside Telegram');
        return;
    }

    // Expand to full height
    tg.expand();

    // Ready signal
    tg.ready();

    // Apply Telegram theme colors
    if (tg.themeParams) {
        document.documentElement.style.setProperty(
            '--tg-theme-bg-color',
            tg.themeParams.bg_color || '#0a0a0f'
        );
        document.documentElement.style.setProperty(
            '--tg-theme-text-color',
            tg.themeParams.text_color || '#ffffff'
        );
        document.documentElement.style.setProperty(
            '--tg-theme-button-color',
            tg.themeParams.button_color || '#6366f1'
        );
    }

    // Enable closing confirmation if needed
    // tg.enableClosingConfirmation();

    console.log('Telegram WebApp initialized', {
        version: tg.version,
        platform: tg.platform,
        colorScheme: tg.colorScheme
    });
}

// ============================================
// Storage Functions
// ============================================
function loadState() {
    try {
        // Load news count
        const savedCount = localStorage.getItem(CONFIG.STORAGE_KEYS.NEWS_COUNT);
        state.newsCount = savedCount ? parseInt(savedCount, 10) : 0;

        // Load visited countries
        const savedCountries = localStorage.getItem(CONFIG.STORAGE_KEYS.COUNTRIES_VISITED);
        if (savedCountries) {
            state.countriesVisited = new Set(JSON.parse(savedCountries));
        }

        updateUI();
    } catch (e) {
        console.error('Failed to load state:', e);
    }
}

function saveState() {
    try {
        localStorage.setItem(CONFIG.STORAGE_KEYS.NEWS_COUNT, state.newsCount.toString());
        localStorage.setItem(
            CONFIG.STORAGE_KEYS.COUNTRIES_VISITED,
            JSON.stringify([...state.countriesVisited])
        );
    } catch (e) {
        console.error('Failed to save state:', e);
    }
}

// ============================================
// UI Functions
// ============================================
function updateUI() {
    elements.newsCount.textContent = state.newsCount;
}

function showState(stateName) {
    // Hide all states
    elements.welcomeState.classList.add('hidden');
    elements.loadingState.classList.add('hidden');
    elements.newsCard.classList.add('hidden');

    // Show requested state
    switch (stateName) {
        case 'welcome':
            elements.welcomeState.classList.remove('hidden');
            elements.headerTitle.textContent = 'Новости мира';
            break;
        case 'loading':
            elements.loadingState.classList.remove('hidden');
            elements.headerTitle.textContent = '🔍 Ищем...';
            break;
        case 'news':
            elements.newsCard.classList.remove('hidden');
            break;
    }
}

function displayNews(data) {
    const { news, metadata } = data;

    // Update header with country
    elements.headerTitle.textContent = `${metadata.country.flag} ${metadata.country.name}`;

    // Update image
    if (news.image) {
        elements.newsImage.src = news.image;
        elements.newsImage.alt = news.title;
        elements.newsImageContainer.classList.remove('hidden');

        // Handle image load error
        elements.newsImage.onerror = () => {
            elements.newsImageContainer.classList.add('hidden');
        };
    } else {
        elements.newsImageContainer.classList.add('hidden');
    }

    // Update content
    elements.newsTitle.textContent = news.title;
    elements.newsDescription.textContent = news.description || 'Описание недоступно';

    // Update metadata
    elements.newsSource.textContent = news.source || 'Неизвестный источник';
    elements.newsLanguage.textContent = metadata.language.name;

    // Update read more link
    if (news.url) {
        elements.readMoreBtn.href = news.url;
        elements.readMoreBtn.classList.remove('hidden');
    } else {
        elements.readMoreBtn.classList.add('hidden');
    }

    // Store current news for sharing
    state.currentNews = { news, metadata };

    // Track visited country
    const countryCode = metadata.country.name_en?.toLowerCase() || 'unknown';
    state.countriesVisited.add(countryCode);

    showState('news');
}

// ============================================
// API Functions
// ============================================
async function fetchRandomNews() {
    if (state.isLoading) return;

    state.isLoading = true;
    elements.fetchBtn.disabled = true;
    showState('loading');

    try {
        const response = await fetch(`${CONFIG.API_URL}/api/random-news`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            // Increment counter
            state.newsCount++;
            updateUI();
            saveState();

            // Display news
            displayNews(data);

            // Haptic feedback if available
            if (tg?.HapticFeedback) {
                tg.HapticFeedback.impactOccurred('medium');
            }
        } else {
            throw new Error(data.error || 'Unknown error');
        }

    } catch (error) {
        console.error('Failed to fetch news:', error);

        // Show error state (go back to welcome with error)
        showState('welcome');

        // Show alert
        if (tg?.showAlert) {
            tg.showAlert('Не удалось загрузить новость. Попробуйте ещё раз!');
        } else {
            alert('Не удалось загрузить новость. Попробуйте ещё раз!');
        }

        // Haptic feedback for error
        if (tg?.HapticFeedback) {
            tg.HapticFeedback.notificationOccurred('error');
        }

    } finally {
        state.isLoading = false;
        elements.fetchBtn.disabled = false;
    }
}

// ============================================
// Share Function
// ============================================
function shareNews() {
    if (!state.currentNews) return;

    const { news, metadata } = state.currentNews;
    const shareText = `${metadata.country.flag} ${news.title}\n\n${news.description?.slice(0, 200)}...\n\n📰 ${news.source}`;

    // Try Telegram share first
    if (tg?.shareToStory) {
        // Telegram story sharing (if available)
        tg.shareToStory(news.url);
    } else if (navigator.share) {
        // Web Share API
        navigator.share({
            title: news.title,
            text: shareText,
            url: news.url
        }).catch(console.error);
    } else if (tg) {
        // Fallback: copy to clipboard in Telegram
        navigator.clipboard.writeText(`${shareText}\n\n🔗 ${news.url}`)
            .then(() => {
                tg.showAlert('Скопировано в буфер обмена!');
            })
            .catch(console.error);
    } else {
        // Regular web fallback
        navigator.clipboard.writeText(`${shareText}\n\n🔗 ${news.url}`)
            .then(() => alert('Скопировано в буфер обмена!'))
            .catch(console.error);
    }

    // Haptic feedback
    if (tg?.HapticFeedback) {
        tg.HapticFeedback.impactOccurred('light');
    }
}

// ============================================
// Event Listeners
// ============================================
function initEventListeners() {
    // Main fetch button (welcome state)
    elements.fetchBtn.addEventListener('click', fetchRandomNews);

    // Fetch button in news card
    const fetchBtnNews = document.getElementById('fetch-btn-news');
    if (fetchBtnNews) {
        fetchBtnNews.addEventListener('click', fetchRandomNews);
    }

    // Share button
    elements.shareBtn.addEventListener('click', shareNews);

    // Keyboard shortcut (Space or Enter to fetch)
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' || e.code === 'Enter') {
            if (!state.isLoading && document.activeElement === document.body) {
                e.preventDefault();
                fetchRandomNews();
            }
        }
    });
}

// ============================================
// Initialization
// ============================================
function init() {
    console.log('🌍 Random World News initializing...');

    // Initialize Telegram WebApp
    initTelegram();

    // Load saved state
    loadState();

    // Initialize event listeners
    initEventListeners();

    // Show initial state
    showState('welcome');

    console.log('✅ Random World News ready!');
}

// Start the app
document.addEventListener('DOMContentLoaded', init);
