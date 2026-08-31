const C = 'bblib-v2';
const SHELL = ['./index.html', './assets/bb-logo.png', './manifest.json'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(C).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks =>
    Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
const NULL_CFG = () =>
  new Response('window.CFG=window.CFG||null;', {headers: {'Content-Type': 'text/javascript'}});
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  // Client config: network first so an SM's edit shows on the next open, the
  // last good copy as the offline fallback, and a 404 PURGES the copy so an
  // offboarded client's cached library dies on its first online open.
  if (u.pathname.includes('/cfg/')) {
    e.respondWith(fetch(e.request).then(res => {
      if (res.ok) {
        const cp = res.clone();
        caches.open(C).then(c => c.put(e.request, cp));
        return res;
      }
      caches.open(C).then(c => c.delete(e.request));
      return u.pathname.endsWith('.js') ? NULL_CFG() : res;
    }).catch(() => caches.match(e.request).then(hit =>
      hit || (u.pathname.endsWith('.js') ? NULL_CFG() : Response.error()))));
    return;
  }
  // Navigations: NETWORK FIRST, cache only as the offline fallback, per
  // landmine L-BSWL-020. Cache-first HTML ships every future deploy to nobody.
  if (e.request.mode === 'navigate') {
    e.respondWith(fetch(e.request).then(res => {
      const cp = res.clone();
      caches.open(C).then(c => c.put('./index.html', cp));
      return res;
    }).catch(() => caches.match('./index.html')));
    return;
  }
  // Static assets stay cache first.
  e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request)));
});
