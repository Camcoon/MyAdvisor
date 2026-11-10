// Browser-computed checks of rendered templates; no server, cookie or UAT run.
// Uses a dedicated installed Chromium profile and loopback debugging endpoint.
const {spawn} = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

async function main() {
  const [browser, htmlFile] = process.argv.slice(2);
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'MyAdvisor-Contrast-'));
  const child = spawn(browser, ['--headless=new', '--disable-gpu', '--no-first-run',
    '--no-default-browser-check', '--remote-debugging-address=127.0.0.1',
    '--remote-debugging-port=0', `--user-data-dir=${profile}`],
    {stdio: ['ignore', 'ignore', 'ignore'], windowsHide: true});
  const portFile = path.join(profile, 'DevToolsActivePort');
  const deadline = Date.now() + 12000;
  while (!fs.existsSync(portFile)) {
    if (Date.now() >= deadline) {child.kill();throw new Error('Chromium did not create its local debugging endpoint');}
    await new Promise(resolve => setTimeout(resolve, 50));
  }
  const [port, endpoint] = fs.readFileSync(portFile, 'utf8').trim().split(/\r?\n/);
  const socket = new WebSocket(`ws://127.0.0.1:${port}${endpoint}`);
  await new Promise((resolve, reject) => {
    socket.addEventListener('open', resolve, {once: true});
    socket.addEventListener('error', () => reject(new Error('Local browser debugging connection failed')), {once: true});
  });
  let serial = 0; const pending = new Map();
  const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    if (process.env.CONTRAST_DEBUG) process.stderr.write(method + '\n');
    const id = ++serial;
    pending.set(id, {resolve, reject});
    socket.send(JSON.stringify({id, method, params, ...(sessionId ? {sessionId} : {})}));
  });
  socket.addEventListener('message', data => {
      const message = JSON.parse(data.data);
      const waiter = pending.get(message.id);
      if (waiter) {
        pending.delete(message.id);
        message.error ? waiter.reject(new Error(message.error.message)) : waiter.resolve(message.result);
      }
  });
  child.on('error', error => {for (const entry of pending.values()) entry.reject(error);});
  const timeout = setTimeout(() => {child.kill(); process.stderr.write('Browser contrast probe timed out\n'); process.exitCode = 1;}, 25000);
  try {
    const version = await send('Browser.getVersion');
    const {targetId} = await send('Target.createTarget', {url: 'about:blank'});
    const {sessionId} = await send('Target.attachToTarget', {targetId, flatten: true});
    const command = (method, params) => send(method, params, sessionId);
    await command('Page.enable');
    await command('DOM.enable');
    await command('CSS.enable');
    const {frameTree} = await command('Page.getFrameTree');
    await command('Page.setDocumentContent', {frameId: frameTree.frame.id, html: fs.readFileSync(htmlFile, 'utf8')});
    const measure = async () => {
      const result = await command('Runtime.evaluate', {expression: `(() => {
        const samples = [...document.querySelectorAll('.course-review-table th, .course-review-table td, .plan-status-alert p')];
        function rgb(value) { return value.match(/[\\d.]+/g).slice(0,3).map(Number); }
        function luminance(color) { return color.map(c => {c /= 255; return c <= .04045 ? c/12.92 : ((c+.055)/1.055)**2.4;}).reduce((s,c,i)=>s+c*[.2126,.7152,.0722][i],0); }
        function background(el) { for(let n=el;n;n=n.parentElement) { const value=getComputedStyle(n).backgroundColor; if(value !== 'rgba(0, 0, 0, 0)' && value !== 'transparent') return value; } return 'rgb(255, 255, 255)'; }
        return samples.filter(el=>el.textContent.trim()).map(el => {
          const style=getComputedStyle(el);
          // Bootstrap draws table hover backgrounds using an inset shadow.
          const state=el.closest('tr')?.matches(':hover') ? getComputedStyle(el.closest('table')).getPropertyValue('--bs-table-hover-bg').trim() : '';
          const fg=style.color, bg=state || background(el);
          const a=luminance(rgb(fg));
          const resolvedBg = bg.startsWith('#') ? [1,3,5].map(i=>parseInt(bg.slice(i,i+2),16)) : rgb(bg);
          const b=luminance(resolvedBg);
          return {text:el.textContent.trim(),foreground:fg,background:bg,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
        });
      })()`, returnByValue: true});
      if (result.exceptionDetails) throw new Error('Contrast evaluation failed');
      return result.result.value;
    };
    const normal = await measure();
    const {root} = await command('DOM.getDocument');
    const {nodeId} = await command('DOM.querySelector', {nodeId: root.nodeId, selector: '.course-review-table tbody tr'});
    let hover = [];
    if (nodeId) {
      await command('CSS.forcePseudoState', {nodeId, forcedPseudoClasses: ['hover']});
      hover = await measure();
    }
    process.stdout.write(JSON.stringify({browser:version.product,source:'Real rendered template; pinned CSS; no network/auth cookies',normal,hover}));
  } finally {
    clearTimeout(timeout);
    socket.send(JSON.stringify({id: ++serial, method: 'Browser.close'}));
    socket.close();
    child.kill(); // Dedicated temporary browser only; user's browser is never attached.
  }
}
main().catch(error => {process.stderr.write(error.message+'\n');process.exitCode=1;});
