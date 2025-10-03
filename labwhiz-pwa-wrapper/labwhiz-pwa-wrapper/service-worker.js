const CACHE = "labwhiz-pwa-v1";
const ASSETS = [
  "/",
  "/index.html",
  "/manifest.json",
  "/install.js",
  "/offline.html",
  "/icons/icon-192.png",
  "/icons/icon-512.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  const req = event.request;

  // App shell: serve from cache first
  if (ASSETS.includes(new URL(req.url).pathname)) {
    event.respondWith(
      caches.match(req).then((cached) => cached || fetch(req))
    );
    return;
  }

  // Navigations: try network, fallback to offline page
  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req).catch(() => caches.match("/offline.html"))
    );
    return;
  }

  // Default: network first, fallback to cache
  event.respondWith(
    fetch(req).then((res) => {
      const resClone = res.clone();
      caches.open(CACHE).then((cache) => cache.put(req, resClone));
      return res;
    }).catch(() => caches.match(req))
  );
});
