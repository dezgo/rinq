// Tina Phone Service Worker
// Minimal SW to enable PWA installation

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

// Pass through all fetch requests (no offline caching needed)
self.addEventListener('fetch', (event) => {
    event.respondWith(fetch(event.request));
});
