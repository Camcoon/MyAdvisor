// Static artifact validation only. Does not start the app, connect to a DB,
// execute Postman scripts, or establish that any HTTP assertion passes.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '../../..');
const collectionPath = path.join(__dirname, 'MyAdvisor-Assignment2.postman_collection.json');
const collection = JSON.parse(fs.readFileSync(collectionPath, 'utf8'));
assert.equal(collection.info.schema, 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json');
assert.equal(collection.auth.type, 'noauth');
const variables = new Map(collection.variable.map(v => [v.key, v.value]));
assert.equal(variables.size, collection.variable.length);
for (const [key, value] of variables) {
  if (/password|token|_id$|baseline|foreign_error/.test(key)) assert.equal(value, '', `Exported value must be blank: ${key}`);
}
const routes = [];
for (const [file, prefix] of [
  ['app/routers/advising_api.py', '/api'], ['app/routers/users.py', '/api'],
  ['app/routers/login.py', ''], ['app/routers/register.py', ''],
  ['app/routers/logout.py', ''], ['app/main.py', ''],
]) {
  const source = fs.readFileSync(path.join(root, file), 'utf8');
  const decorators = /@(?:api_router|router|app)\.(get|post|put|delete)\(\s*["']([^"']+)["']/g;
  for (const m of source.matchAll(decorators)) {
    const url = prefix + m[2];
    routes.push({method: m[1].toUpperCase(), url,
      regex: new RegExp('^' + url.replace(/\{[^}]+\}/g, '[^/]+') + '$')});
  }
}
let scripts = 0;
let count = 0;
const covered = new Set();
function validateUrl(url, name) {
  const label = `Invalid Postman URL: ${name}`;
  assert.ok(url && typeof url === 'object' && !Array.isArray(url), label);
  assert.equal(typeof url.raw, 'string', label);
  assert.match(url.raw, /^\{\{base_url\}\}\/[^\s?#]+$/, label);
  // A raw-only object can pass route checks yet import as an empty URL.
  // Include the structured components used by Postman to build the URL.
  assert.deepEqual(url.host, ['{{base_url}}'], label);
  assert.ok(Array.isArray(url.path) && url.path.length > 0, label);
  assert.ok(url.path.every(segment => typeof segment === 'string' && segment.length > 0 && !segment.includes('/')), label);
  assert.equal(url.raw, `{{base_url}}/${url.path.join('/')}`, label);
  assert.deepEqual(Object.keys(url).sort(), ['host', 'path', 'raw'], label);
  const resolved = url.raw.replace(/\{\{([^{}]+)\}\}/g, (_, key) => {
    assert.ok(variables.has(key), `Undeclared URL variable: ${key}`);
    return key === 'base_url' ? variables.get(key) : '1';
  });
  const parsed = new URL(resolved);
  assert.ok(['http:', 'https:'].includes(parsed.protocol), label);
  assert.ok(parsed.hostname, label);
}
function events(owner) {
  for (const event of owner.event || []) {
    const code = event.script.exec.join('\n');
    assert.doesNotMatch(code, /pm\.response\.cookies\.get\s*\(/,
      'Read authentication cookies from Set-Cookie headers; the response cookie lookup may be empty.');
    new vm.Script(code, {filename: `${owner.name || 'collection'}-${event.listen}.js`});
    scripts++;
  }
}
events(collection);
for (const folder of collection.item) {
  events(folder);
  for (const item of folder.item) {
    count++;
    assert.equal(item.name.slice(0, 2), String(count).padStart(2, '0'));
    events(item);
    const request = item.request;
    validateUrl(request.url, item.name);
    const url = request.url.raw.replace('{{base_url}}', '').split('?')[0];
    const route = routes.find(r => r.method === request.method && r.regex.test(url));
    assert.ok(route, `Unimplemented method/path: ${item.name}`);
    covered.add(`${route.method} ${route.url}`);
    assert.equal(item.protocolProfileBehavior.followRedirects, false);
    assert.equal(item.protocolProfileBehavior.disableCookies, true);
    const test = item.event.find(e => e.listen === 'test').script.exec.join('\n');
    assert.match(test, /pm\.response\.to\.have\.status\(\d+\)/);
    assert.match(test, /setNextRequest\(null\)/);
    for (const m of JSON.stringify(item).matchAll(/\{\{([^{}]+)\}\}/g)) {
      assert.ok(m[1].startsWith('$') || variables.has(m[1]), `Undeclared variable: ${m[1]}`);
    }
    if (request.body?.mode === 'raw' && !item.name.includes('Malformed JSON')) {
      const body = request.body.raw.replace(/\{\{[^{}]+\}\}/g, '1');
      JSON.parse(body);
    }
    if (url.includes('/semester-plans/') || url.includes('/advisor/plans/')) {
      // Numeric 0 and a reserved missing-resource sentinel are negative cases.
      for (const id of url.matchAll(/\/(\d+)(?=\/|$)/g)) assert.ok(['0','2147483647'].includes(id[1]), 'Hardcoded fixture plan ID');
    }
  }
}
const apiRoutes = routes.filter(r => r.url.startsWith('/api/'));
for (const route of apiRoutes) assert.ok(covered.has(`${route.method} ${route.url}`), `Missing API operation ${route.url}`);
assert.equal(count, 90);
assert.equal(apiRoutes.length, 15);
console.log(`Static checks passed: valid JSON, ${count} requests, ${scripts} JavaScript scripts compile, all ${apiRoutes.length} API operations covered.`);
console.log('Structured URLs, methods/paths, variables, body JSON, blank exported credentials, and redirect/cookie settings checked.');
console.log('Postman/Newman runtime execution: NOT PERFORMED.');
