const C = 'bblib-v1';
const SHELL = ['./', './index.html', './assets/bb-logo.png', './manifest.json'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(C).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks =>
    Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (u.pathname.includes('/cfg/')) {
    e.respondWith(fetch(e.request).catch(() =>
      new Response('window.CFG=window.CFG||null;', {headers:{'Content-Type':'text/javascript'}})));
    return;
  }
  e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request)));
});
