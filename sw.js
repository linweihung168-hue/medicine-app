const CACHE_NAME = 'find-medicine-v4';
const ASSETS = ['./', './index.html', './manifest.json', './icon-192.png', './icon-512.png', './line-icon.png'];
const FETCH_TIMEOUT = 3000; // 網路太慢時,等這麼久就直接用快取,不要一直卡著

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
  );
  self.clients.claim();
});

function fetchWithTimeout(request, ms) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('timeout')), ms);
    fetch(request).then((res) => { clearTimeout(timer); resolve(res); }).catch((err) => { clearTimeout(timer); reject(err); });
  });
}

self.addEventListener('fetch', (e) => {
  if (e.request.url.includes('script.google.com')) return;
  // 網路優先,但太慢(超過 FETCH_TIMEOUT)或失敗就退回快取,更新永遠會生效、離線或訊號差也不會卡住
  e.respondWith(
    fetchWithTimeout(e.request, FETCH_TIMEOUT).then((res) => {
      const resClone = res.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
      return res;
    }).catch(() => caches.match(e.request))
  );
});
