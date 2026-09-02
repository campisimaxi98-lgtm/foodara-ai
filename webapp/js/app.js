/* FOODARA - Main app logic */

const app = (() => {
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);

  let currentView = 'dashboard';
  let currentPantryCat = 'Todos';
  let editingFoodId = null;
  let purchaseDraft = [];

  const months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
  const weekDays = ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];

  function toast(msg) {
    const t = $('#toast');
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._t);
    t._t = setTimeout(() => t.classList.remove('show'), 2600);
  }

  function formatMoney(n) { return '$' + Math.round(n || 0).toLocaleString('es-AR'); }

  function today() { return new Date().toISOString().slice(0,10); }
  function daysLeft(dateStr) {
    if (!dateStr) return null;
    const exp = new Date(dateStr + 'T23:59:59');
    const t = new Date(); t.setHours(23,59,59,0);
    return Math.ceil((exp - t) / (1000 * 3600 * 24));
  }

  /* ================= AUTH ================= */
  let isLoginMode = true;
  const user = Store.getSession();

  function showAuth() {
    $('#app').classList.add('hidden');
    $('#authScreen').classList.remove('hidden');
  }
  function showApp() {
    $('#authScreen').classList.add('hidden');
    $('#app').classList.remove('hidden');
    renderAll();
  }

  function initAuth() {
    $('#authSwitch').addEventListener('click', (e) => {
      e.preventDefault();
      isLoginMode = !isLoginMode;
      $('#authTitle').textContent = isLoginMode ? 'Bienvenido' : 'Crear cuenta';
      $('#authSub').textContent = isLoginMode ? 'Ingresá a tu sistema inteligente de alimentos' : 'Empezá a gestionar tu alimentación';
      $('#authBtn').textContent = isLoginMode ? 'Ingresar' : 'Crear cuenta';
      $('#nameField').style.display = isLoginMode ? 'none' : 'flex';
      $('#authError').textContent = '';
      $('#authPassword').autocomplete = isLoginMode ? 'current-password' : 'new-password';
    });

    $('#authForm').addEventListener('submit', (e) => {
      e.preventDefault();
      const email = $('#authEmail').value.trim();
      const pass = $('#authPassword').value;
      const err = $('#authError');
      err.textContent = '';

      if (isLoginMode) {
        const r = Store.login(email, pass);
        if (r.error) { err.textContent = r.error; return; }
        Store.setSession(r.user);
      } else {
        const name = $('#authName').value.trim();
        if (!name) { err.textContent = 'Ingresá tu nombre.'; return; }
        if (pass.length < 4) { err.textContent = 'La contraseña debe tener al menos 4 caracteres.'; return; }
        const r = Store.register(name, email, pass);
        if (r.error) { err.textContent = r.error; return; }
        Store.setSession(r.user);
      }
      showApp();
      toast('¡Bienvenido! 🎉');
    });

    if (user) {
      // Prefill
      $('#authEmail').value = user.email;
    }
    if (!user) showAuth(); else showApp();
  }

  $('#logoutBtn').addEventListener('click', () => {
    Store.setSession(null);
    location.reload();
  });

  /* ================= NAVIGATION ================= */
  function go(view) {
    currentView = view;
    $$('.view').forEach(v => v.classList.remove('active'));
    const target = $('#view-' + view);
    if (target) target.classList.add('active');
    $$('.nav-link, .nav-item').forEach(n => {
      n.classList.toggle('active', n.dataset.view === view);
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (view === 'ai') renderSuggestions();
  }

  function bindNav() {
    $$('.nav-link, .nav-item').forEach(el => {
      el.addEventListener('click', () => go(el.dataset.view));
    });
    $$('[data-goto]').forEach(el => {
      el.addEventListener('click', () => {
        const act = el.dataset.act;
        go(el.dataset.goto);
        if (act === 'add-food') setTimeout(() => openCapture('pantry'), 300);
        if (act === 'add-purchase') setTimeout(() => openCapture('purchase'), 300);
        if (act === 'add-meal') setTimeout(() => openCapture('meal'), 300);
      });
    });
  }

  /* ================= RENDER ================= */
  function renderAll() {
    const db = Store.getDB();
    const u = Store.getSession();
    const todayStr = today();

    // user
    const firstName = (u?.name || 'Maximiliano').split(' ')[0];
    $('#userName').textContent = firstName;
    $('#profileName').textContent = u?.name || 'Maximiliano';
    $('#profileEmail').textContent = u?.email || 'tu@email.com';
    const initials = firstName.charAt(0).toUpperCase();
    $('#profileChip').textContent = initials;
    $('#profileAvatar').textContent = initials;

    // date
    const d = new Date();
    $('#todayDate').textContent = `${weekDays[d.getDay()]}, ${d.getDate()} de ${months[d.getMonth()]}`;
    $('#nutriDate').textContent = `${weekDays[d.getDay()]}, ${d.getDate()} de ${months[d.getMonth()]}`;

    renderDashboard(db, todayStr);
    renderNutrition(db, todayStr);
    renderPantry(db);
    renderPurchases(db, todayStr);
    renderAnalytics(db, todayStr);

    // goals
    $('#goalCal').value = db.goals.cal;
    $('#goalProt').value = db.goals.prot;
    $('#goalCarb').value = db.goals.carb;
    $('#goalFat').value = db.goals.fat;

    // api
    $('#apiUrl').value = apiUrl || '';
  }

  /* Dashboard */
  function renderDashboard(db, todayStr) {
    const thisMonth = todayStr.slice(0,7);
    const spent = db.purchases.filter(p => (p.date||'').slice(0,7) === thisMonth).reduce((s,p)=>s+(+p.total||0),0);
    // eject arroz comparison: vs previous month
    const prevMonth = new Date(); prevMonth.setMonth(prevMonth.getMonth()-1);
    const prevKey = prevMonth.toISOString().slice(0,7);
    const prevSpent = db.purchases.filter(p => (p.date||'').slice(0,7) === prevKey).reduce((s,p)=>s+(+p.total||0),0);
    const diff = prevSpent ? Math.round(((spent - prevSpent) / prevSpent) * 100) : 0;

    $('#mGastos').textContent = formatMoney(spent);
    $('#mGastosSub').textContent = spent === 0 ? 'Sin gastos este mes' : (diff < 0 ? `↓ ${Math.abs(diff)}% vs. mes anterior` : (diff > 0 ? `↑ ${diff}% vs. mes anterior` : 'Igual que el mes anterior'));
    $('#mGastosSub').className = 'metric-sub ' + (diff <= 0 ? 'good' : 'warning');

    const cal = db.meals.filter(m => m.date === todayStr).reduce((s,m)=>s+(+m.cal||0),0);
    $('#mCalorias').textContent = cal;

    $('#mDespensa').textContent = db.pantry.length;
    const expiring = db.pantry.filter(p => { const l = daysLeft(p.expiry); return l !== null && l >= 0 && l <= 3; }).length;
    const expired = db.pantry.filter(p => daysLeft(p.expiry) !== null && daysLeft(p.expiry) < 0).length;
    $('#mDespensaSub').textContent = expiring ? `${expiring} próximos a vencer` : (expired ? `${expired} vencidos` : 'Todo en orden');
    $('#mDespensaSub').className = 'metric-sub ' + (expiring || expired ? 'warning' : 'good');

    const waste = db.pantry.length ? Math.round((expired / db.pantry.length) * 100) : 0;
    $('#mDesperdicio').textContent = waste + '%';
    // subclass handled
  }

  /* Nutrition */
  function renderNutrition(db, todayStr) {
    const meals = db.meals.filter(m => m.date === todayStr);
    const cal = meals.reduce((s,m)=>s+(+m.cal||0),0);
    const prot = meals.reduce((s,m)=>s+(+m.prot||0),0);
    const carb = meals.reduce((s,m)=>s+(+m.carb||0),0);
    const fat = meals.reduce((s,m)=>s+(+m.fat||0),0);
    const g = db.goals;

    $('#nCal').textContent = cal + ' kcal';
    $('#nProt').textContent = Math.round(prot) + 'g';
    $('#nCarb').textContent = Math.round(carb) + 'g';
    $('#nFat').textContent = Math.round(fat) + 'g';

    const bars = [
      ['Calorías', cal, g.cal],
      ['Proteínas', prot, g.prot],
      ['Carbohidratos', carb, g.carb],
      ['Grasas', fat, g.fat]
    ];
    $('#macroBars').innerHTML = bars.map(([name, val, goal]) => {
      const pct = Math.min(100, Math.round((val / goal) * 100));
      return `<div class="macro-row">
        <span class="macro-label">${name}</span>
        <div class="macro-track"><div class="macro-fill" style="width:${pct}%"></div></div>
        <span class="macro-val">${Math.round(val)} / ${goal}</span>
      </div>`;
    }).join('');

    const list = $('#mealList');
    if (meals.length === 0) { list.className = 'list-empty'; list.textContent = 'No registraste comidas hoy.'; }
    else {
      list.className = '';
      list.innerHTML = meals.slice().reverse().map(m => `
        <div class="entry-item">
          <div class="entry-main"><h4>${escapeHtml(m.name)}</h4><p>${Math.round(m.cal)} kcal · P ${m.prot}g · C ${m.carb}g · G ${m.fat}g</p></div>
          <div class="entry-right"><button class="entry-del" data-del-meal="${m.id}">✕</button></div>
        </div>`).join('');
    }

    $$('[data-del-meal]').forEach(b => b.addEventListener('click', () => {
      Store.commit(db => { db.meals = db.meals.filter(m => m.id !== b.dataset.delMeal); });
      renderNutrition(Store.getDB(), todayStr);
      renderDashboard(Store.getDB(), todayStr);
      toast('Comida eliminada');
    }));
  }

  /* Pantry */
  function renderPantry(db) {
    $('#pantryCount').textContent = `${db.pantry.length} alimento(s) en tu despensa`;

    const cats = ['Todos', ...new Set(db.pantry.map(p => p.cat))];
    $('#pantryFilter').innerHTML = cats.map(c =>
      `<button class="chip ${currentPantryCat === c ? 'active' : ''}" data-cat="${c}">${c}</button>`).join('');
    $$('#pantryFilter .chip').forEach(ch => ch.addEventListener('click', () => {
      currentPantryCat = ch.dataset.cat; renderPantry(db);
    }));

    const filtered = currentPantryCat === 'Todos' ? db.pantry : db.pantry.filter(p => p.cat === currentPantryCat);
    const grid = $('#pantryGrid');
    if (filtered.length === 0) {
      grid.innerHTML = '<div class="list-empty">No hay alimentos en esta categoría.</div>';
      return;
    }
    grid.innerHTML = filtered.map(p => {
      const left = daysLeft(p.expiry);
      let tag = '';
      if (left !== null) {
        if (left < 0) tag = '<span class="tag expired">VENCIDO</span>';
        else if (left === 0) tag = '<span class="tag exp">Vence hoy</span>';
        else if (left <= 3) tag = `<span class="tag exp">${left} día(s)</span>`;
        else tag = '<span class="tag ok">OK</span>';
      }
      const cls = left !== null ? (left < 0 ? 'expired' : (left <= 3 ? 'expiring' : '')) : '';
      return `<div class="card pantry-item ${cls}">
        <button class="del-btn" data-del-food="${p.id}">✕</button>
        <div class="qty">${p.qty} <small>${p.unit}</small></div>
        <h4>${escapeHtml(p.name)}</h4>
        <p class="p-sub">${p.cat}</p>
        ${tag}
        ${p.price ? `<p class="p-sub" style="margin-top:4px">${formatMoney(p.price)}</p>` : ''}
      </div>`;
    }).join('');

    $$('[data-del-food]').forEach(b => b.addEventListener('click', () => {
      Store.commit(db2 => { db2.pantry = db2.pantry.filter(p => p.id !== b.dataset.delFood); });
      renderAll();
      toast('Alimento eliminado');
    }));
  }

  function openFoodDialog(food) {
    editingFoodId = food ? food.id : null;
    $('#foodDialog').showModal();
    $('#fName').value = food ? food.name : '';
    $('#fQty').value = food ? food.qty : 1;
    $('#fUnit').value = food ? food.unit : 'unidad';
    $('#fExpiry').value = food ? (food.expiry || '') : '';
    $('#fCat').value = food ? food.cat : 'Lácteos';
    $('#fPrice').value = food ? food.price : 0;
    setTimeout(() => $('#fName').focus(), 50);
  }

  function initPantry() {
    $('#addFoodBtn').addEventListener('click', () => openCapture('pantry'));
    $('#foodForm').addEventListener('submit', (e) => {
      e.preventDefault();
      const name = $('#fName').value.trim();
      if (!name) return;
      const data = {
        name,
        qty: +$('#fQty').value || 1,
        unit: $('#fUnit').value,
        expiry: $('#fExpiry').value,
        cat: $('#fCat').value,
        price: +$('#fPrice').value || 0
      };
      Store.commit(db => {
        if (editingFoodId) {
          const idx = db.pantry.findIndex(p => p.id === editingFoodId);
          if (idx >= 0) db.pantry[idx] = { ...db.pantry[idx], ...data, id: editingFoodId };
        } else {
          db.pantry.push({ id: Store.uid(), ...data, added: today() });
        }
      });
      $('#foodDialog').close();
      editingFoodId = null;
      renderAll();
      toast(editingFoodId ? 'Alimento actualizado' : 'Alimento agregado a tu despensa');
    });
    $$('#foodForm [data-close], .modal [data-close]').forEach(b =>
      b.addEventListener('click', () => b.closest('dialog').close()));
  }

  /* Purchases */
  function renderPurchases(db, todayStr) {
    const thisMonth = todayStr.slice(0,7);
    const monthPurchases = db.purchases.filter(p => (p.date||'').slice(0,7) === thisMonth);
    const monthTotal = monthPurchases.reduce((s,p)=>s+(+p.total||0),0);
    const avg = monthPurchases.length ? monthTotal / monthPurchases.length : 0;

    $('#sTotal').textContent = formatMoney(monthTotal);
    $('#sTotalSub').textContent = monthPurchases.length ? `${monthPurchases.length} compra(s) este mes` : 'Sin datos este mes';
    $('#sAvg').textContent = formatMoney(avg);
    $('#sCount').textContent = db.purchases.length;
    $('#sSave').textContent = formatMoney(Math.round(monthTotal * 0.12));
    $('#shopCount').textContent = `${db.purchases.length} compra(s) registradas`;

    const list = $('#purchaseList');
    if (db.purchases.length === 0) { list.className = 'list-empty'; list.textContent = 'Aún no registraste compras.'; }
    else {
      list.className = '';
      list.innerHTML = db.purchases.slice().reverse().map(p => {
        const d = p.date ? new Date(p.date + 'T00:00:00') : null;
        const dateStr = d ? `${d.getDate()} de ${months[d.getMonth()]}` : '';
        return `<div class="entry-item">
          <div class="entry-main"><h4>${escapeHtml(p.store || 'Compra')}</h4><p>${dateStr} · ${p.items.length} item(s)</p></div>
          <div class="entry-right"><strong>${formatMoney(p.total)}</strong><button class="entry-del" data-del-pur="${p.id}">✕</button></div>
        </div>`;
      }).join('');
    }
    $$('[data-del-pur]').forEach(b => b.addEventListener('click', () => {
      Store.commit(db2 => { db2.purchases = db2.purchases.filter(p => p.id !== b.dataset.delPur); });
      renderAll();
      toast('Compra eliminada');
    }));
  }

  function addPurchaseRow(name, qty, price) {
    const container = $('#purchaseItems');
    const row = document.createElement('div');
    row.className = 'purchase-item-row';
    row.innerHTML = `
      <input type="text" class="pi-name" placeholder="Producto" value="${escapeHtml(name||'')}">
      <input type="number" class="pi-qty" placeholder="Cant." value="${qty != null ? qty : 1}" min="1" step="1">
      <input type="number" class="pi-price" placeholder="Precio $" value="${price != null ? price : ''}" min="0" step="0.01">
      <button type="button" class="entry-del pi-del">✕</button>`;
    row.querySelector('.pi-del').addEventListener('click', () => { row.remove(); updatePurchaseTotal(); });
    ['pi-qty','pi-price'].forEach(cls => row.querySelector('.'+cls).addEventListener('input', updatePurchaseTotal));
    container.appendChild(row);
  }

  function updatePurchaseTotal() {
    let t = 0;
    $$('#purchaseItems .purchase-item-row').forEach(row => {
      const price = +row.querySelector('.pi-price').value || 0;
      const qty = +row.querySelector('.pi-qty').value || 1;
      t += price * qty;
    });
    $('#pTotalPreview').textContent = formatMoney(t);
  }

  function openPurchaseDialog() {
    $('#purchaseDialog').showModal();
    $('#pDate').value = today();
    $('#purchaseItems').innerHTML = '';
    addPurchaseRow('', 1, '');
    updatePurchaseTotal();
    setTimeout(() => $('#pStore').focus(), 50);
  }

  function initPurchases() {
    $('#addPurchaseBtn').addEventListener('click', () => openCapture('purchase'));
    $('#addItemBtn').addEventListener('click', () => addPurchaseRow('', 1, ''));
    $('#purchaseForm').addEventListener('submit', (e) => {
      e.preventDefault();
      const items = [];
      $$('#purchaseItems .purchase-item-row').forEach(row => {
        const name = row.querySelector('.pi-name').value.trim();
        if (!name) return;
        items.push({
          name,
          qty: +row.querySelector('.pi-qty').value || 1,
          price: +row.querySelector('.pi-price').value || 0
        });
      });
      if (items.length === 0) { toast('Agregá al menos un producto'); return; }
      const total = items.reduce((s, i) => s + i.price * i.qty, 0);
      Store.commit(db => {
        db.purchases.push({ id: Store.uid(), store: $('#pStore').value.trim() || 'Supermercado', date: $('#pDate').value || today(), items, total });
      });
      $('#purchaseDialog').close();
      renderAll();
      toast('Compra registrada 🛒');
    });
    $$('#purchaseForm [data-close]').forEach(b => b.addEventListener('click', () => b.closest('dialog').close()));
  }

  /* Analytics */
  function renderAnalytics(db, todayStr) {
    // last 7 days chart
    const map = {};
    for (let i = 6; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      map[d.toISOString().slice(0,10)] = 0;
    }
    db.purchases.forEach(p => { if (p.date && p.date in map) map[p.date] += (+p.total||0); });
    const max = Math.max(...Object.values(map), 1);
    $('#expenseChart').innerHTML = Object.entries(map).map(([date, val]) =>
      `<div class="bar" style="height:${Math.max(5, (val/max)*100)}%"><span>${val ? formatMoney(val) : ''}</span></div>`).join('');
    $('#chartDays').innerHTML = Object.keys(map).map(date => {
      const d = new Date(date + 'T00:00:00');
      return `<span>${weekDays[d.getDay()].slice(0,2)}</span>`;
    }).join('');
    $('#rangeLabel').textContent = 'Últimos 7 días';

    // waste avoided
    const expired = db.pantry.filter(p => daysLeft(p.expiry) !== null && daysLeft(p.expiry) < 0).length;
    $('#wasteAvoided').textContent = `${Math.max(0, db.pantry.length - expired)}/${db.pantry.length || 0}`;

    // category distribution
    const catTotal = {};
    db.purchases.forEach(p => p.items.forEach(i => {
      const full = Store.getDB().pantry.find(x => x.name.toLowerCase() === i.name.toLowerCase());
      const cat = full ? full.cat : 'Compra';
      catTotal[cat] = (catTotal[cat] || 0) + (i.price || 0) * (i.qty || 1);
    }));
    const entries = Object.entries(catTotal).sort((a,b)=>b[1]-a[1]);
    const catMax = Math.max(...entries.map(e=>e[1]), 1);
    $('#categoryBars').innerHTML = entries.length ? entries.map(([cat, val]) =>
      `<div class="cat-row"><span class="cat-name">${escapeHtml(cat)}</span>
       <div class="cat-track"><div class="cat-fill" style="width:${(val/catMax)*100}%"></div></div>
       <span class="cat-val">${formatMoney(val)}</span></div>`).join('')
      : '<span class="muted small">Registrá compras para ver la distribución.</span>';
  }

  /* ================= AI ================= */
  function renderSuggestions() {
    const db = Store.getDB();
    const expiring = db.pantry.filter(p => { const l = daysLeft(p.expiry); return l !== null && l <= 3; });
    const sugs = [];
    if (db.pantry.length) sugs.push('¿Qué tengo en la despensa?');
    if (expiring.length) sugs.push(`¿Qué me vence pronto?`);
    sugs.push('¿Cuánto gasté este mes?');
    sugs.push('¿Cuántas calorías comí hoy?');
    $('#aiSuggestions').innerHTML = sugs.map(s => `<button type="button">${s}</button>`).join('');
    $$('#aiSuggestions button').forEach(b => b.addEventListener('click', () => {
      $('#chatField').value = b.textContent;
      submitChat();
    }));
  }

  function addMsg(role, html) {
    const body = $('#chatBody');
    const div = document.createElement('div');
    div.className = 'msg ' + role;
    div.innerHTML = `<div class="bubble">${html}</div>`;
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
  }

  function submitChat() {
    const field = $('#chatField');
    const text = field.value.trim();
    if (!text) return;
    field.value = '';
    addMsg('user', escapeHtml(text));
    addMsg('bot', '<span class="typing"><span></span><span></span><span></span></span>');
    const body = $('#chatBody');
    setTimeout(() => {
      // remove typing
      const msgs = body.querySelectorAll('.msg');
      const last = msgs[msgs.length - 1];
      if (last && last.querySelector('.typing')) {
        // replace typing bubble with answer
        const answer = FoodaraAI.respond(text);
        last.innerHTML = `<div class="bubble">${answer.html}</div>`;
      }
      body.scrollTop = body.scrollHeight;
    }, 650 + Math.random() * 500);
  }

  function initAI() {
    $('#chatForm').addEventListener('submit', (e) => { e.preventDefault(); submitChat(); });
  }

  /* ================= PROFILE / API ================= */
  let apiUrl = ''; // leave empty -> local mode

  function initProfile() {
    $('#saveGoals').addEventListener('click', () => {
      Store.commit(db => {
        db.goals.cal = +$('#goalCal').value || 2000;
        db.goals.prot = +$('#goalProt').value || 128;
        db.goals.carb = +$('#goalCarb').value || 225;
        db.goals.fat = +$('#goalFat').value || 80;
      });
      renderAll();
      toast('Objetivos guardados ✓');
    });

    $('#saveApi').addEventListener('click', () => {
      const u = $('#apiUrl').value.trim().replace(/\/+$/, '');
      try { localStorage.setItem('foodara_api', u); } catch(e){}
      apiUrl = u;
      const st = $('#apiStatus');
      if (u) { st.textContent = 'Servidor configurado. La app intentará sincronizar. ⚙️'; st.className = 'small good'; }
      else { st.textContent = 'Modo local activado (datos en tu dispositivo).'; st.className = 'small muted'; }
      toast('Configuración guardada');
    });

    $('#resetData').addEventListener('click', () => {
      if (confirm('¿Seguro que querés borrar TODOS tus datos locales?')) {
        Store.reset();
        renderAll();
        toast('Datos restablecidos');
      }
    });
  }

  /* ================= UTIL ================= */
  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
      .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }

  /* ================= CAPTURE (manual / QR / photo) ================= */
  let capTarget = 'pantry';       // pantry | meal | purchase
  let capTab = 'manual';
  let capProduct = null;          // {name, brand, image, cal, prot, carb, fat, barcode}
  let capPhoto = null;            // {dataUrl, fileName}

  const capTitles = { pantry: 'Registrar alimento en despensa', meal: 'Registrar comida (nutrición)', purchase: 'Registrar producto en compra' };
  const capModes = { pantry: 'Elegí cómo registrar el alimento', meal: 'Elegí cómo registrar la comida', purchase: 'Elegí cómo registrar el producto comprado' };

  function setCapPane(tab) {
    capTab = tab;
    $$('#captureTabs .cap-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
    ['manual','qr','photo'].forEach(t => $('#pane-' + t).classList.toggle('hidden', t !== tab));
    if (tab === 'qr') {
      startQr();
    } else {
      FoodaraCapture.stopScan().then(() => FoodaraCapture.releaseStream());
    }
  }

  async function startQr() {
    const st = $('#qrStatus');
    st.textContent = 'Iniciando cámara...';
    try {
      await FoodaraCapture.startScan('qrReader', async (raw) => {
        // stop after first successful decode
        await FoodaraCapture.stopScan();
        await FoodaraCapture.releaseStream();
        st.textContent = 'Código leído ✓';
        const data = await FoodaraCapture.lookUpBarcode(raw);
        applyCapProduct(data);
      });
      st.textContent = 'Apuntá la cámara al código de barras.';
    } catch (e) {
      st.textContent = 'No se pudo acceder a la cámara. Escribilo manualmente o subí una foto.';
    }
  }

  function applyCapProduct(data) {
    const box = $('#qrStatus');
    if (!data.ok) { box.textContent = data.error; return; }
    box.textContent = 'Producto encontrado: ' + data.name;
    capProduct = {
      name: data.name,
      brand: data.brand,
      image: data.image,
      cal: data.cal, prot: data.prot, carb: data.carb, fat: data.fat,
      barcode: data.barcode
    };
    renderCapPreview();
  }

  function renderCapPreview() {
    const bp = $('#capPreview');
    if (!capProduct) { bp.classList.add('hidden'); return; }
    bp.classList.remove('hidden');
    $('#capName').value = capProduct.name || '';
    $('#capImg').src = capProduct.image || '';
    $('#capPName').textContent = capProduct.name || 'Producto';
    $('#capPSub').textContent = capProduct.barcode ? ('EAN ' + capProduct.barcode + (capProduct.brand ? ' · ' + capProduct.brand : '')) : '';
    const nut = $('#capNutri');
    if (capProduct.cal != null) {
      nut.style.display = 'flex';
      $('#capCal').textContent = capProduct.cal;
      $('#capProt').textContent = capProduct.prot != null ? capProduct.prot : '–';
      $('#capCarb').textContent = capProduct.carb != null ? capProduct.carb : '–';
      $('#capFat').textContent = capProduct.fat != null ? capProduct.fat : '–';
    } else {
      nut.style.display = 'none';
    }
  }

  async function openCapture(target) {
    capTarget = target || 'pantry';
    // last tab remembered? default manual
    document.querySelectorAll('dialog').forEach(d => { try { d.close(); } catch(e){} });
    $('#captureTitle').textContent = capTitles[capTarget] || 'Registrar';
    $('#captureMode').textContent = capModes[capTarget] || '';
    $('#capTarget').value = target || 'pantry';

    // clear state
    capProduct = null;
    capPhoto = null;
    $('#capName').value = '';
    $('#capPrice').value = '';
    $('#capExpiry').value = '';
    $('#capQty').value = 1;
    $('#capCat').value = 'Almacén';
    $('#capPreview').classList.add('hidden');
    $('#capNutri').style.display = 'none';
    $('#photoPreview').classList.add('hidden');
    $('#cheaperBox').classList.add('hidden');
    $('#qrResult').innerHTML = '';
    $('#qrStatus').textContent = 'Apuntá la cámara al código de barras del producto.';

    // show/hide expiry depending on target (pantry only)
    $('#expiryField').style.display = capTarget === 'pantry' ? 'flex' : 'none';
    if (capTarget === 'meal') $('#capCat').closest('.field').style.display = 'flex';
    else $('#capCat').closest('.field').style.display = 'flex';

    setCapPane('manual');
    $('#captureDialog').showModal();
    $('#capName').focus();
    $('#captureDialog').dataset.initialized = '1';
  }

  function capCurrentPrice() { return +$('#capPrice').value || 0; }

  function updateCheaper() {
    const name = $('#capName').value.trim();
    const box = $('#cheaperBox');
    if (!name) { box.classList.add('hidden'); return; }
    const res = PriceFinder.findCheaper(name, capCurrentPrice());
    if (!res.found) { box.classList.add('hidden'); return; }
    box.classList.remove('hidden');
    $('#cheaperSub').textContent = res.current ? ('comprando a ' + formatMoney(res.current)) : 'precios típicos';
    let html = '';
    res.options.forEach(o => {
      html += `<div class="cheaper-item">
        <span class="ci-name">${escapeHtml(o.label)}</span>
        <span><span class="ci-price">${formatMoney(o.price)}</span>${o.diff > 0 ? ` <span class="ci-save">−${o.pct}%</span>` : ''}</span>
      </div>`;
    });
    $('#cheaperList').innerHTML = html;
    $('#cheaperTip').textContent = res.tip + (res.totalAnnual ? ` Con el mejor precio podrías ahorrar ~${formatMoney(res.totalAnnual)} por año.` : '');
  }

  function saveCapture() {
    const name = $('#capName').value.trim();
    if (!name) { toast('Escribí o escaneá un producto'); return; }
    const qty = +$('#capQty').value || 1;
    const price = capCurrentPrice();
    const cat = $('#capCat').value;
    const data = { name, qty, unit: $('#capTarget').value === 'pantry' ? ($('#fUnit') ? $('#fUnit').value : 'unidad') : 'unidad', cat, price };

    if (capTarget === 'pantry') {
      data.expiry = $('#capExpiry').value || '';
      // prefill nutrition from captured product
      if (capProduct && capProduct.cal != null) data.nutri = { cal: capProduct.cal, prot: capProduct.prot, carb: capProduct.carb, fat: capProduct.fat };
      Store.commit((db) => db.pantry.push({ id: Store.uid(), ...data, added: today() }));
      toast('Alimento agregado a tu despensa 🥫');
    } else if (capTarget === 'meal') {
      const meal = {
        id: Store.uid(), date: today(), name,
        cal: capProduct && capProduct.cal != null ? Math.round(capProduct.cal * qty) : 0,
        prot: capProduct && capProduct.prot != null ? Math.round(capProduct.prot * qty) : 0,
        carb: capProduct && capProduct.carb != null ? Math.round(capProduct.carb * qty) : 0,
        fat: capProduct && capProduct.fat != null ? Math.round(capProduct.fat * qty) : 0
      };
      Store.commit((db) => db.meals.push(meal));
      toast('Comida registrada 🍽️');
    } else { // purchase
      Store.commit((db) => db.purchases.push({
        id: Store.uid(), store: 'Compra manual', date: today(),
        items: [{ name, qty, price }], total: price * qty
      }));
      toast('Producto agregado a compras 🛒');
    }

    closeCapCapture();
  }

  function closeCapCapture() {
    FoodaraCapture.stopScan().then(() => FoodaraCapture.releaseStream());
    $('#captureDialog').close();
    renderAll();
  }

  function initCapture() {
    $$('#captureTabs .cap-tab').forEach(t => t.addEventListener('click', () => setCapPane(t.dataset.tab)));

    // photo capture
    $('#takePhotoBtn').addEventListener('click', async () => {
      const photo = await FoodaraCapture.pickPhoto();
      if (!photo) return;
      capPhoto = photo;
      $('#photoPreview').classList.remove('hidden');
      $('#photoImg').src = photo.dataUrl;
      $('#photoName').textContent = photo.fileName;
      // use filename heuristic to prefill name + category
      const guess = FoodaraCapture.guessFromFilename(photo.fileName);
      const foodGuess = PriceFinder.match(photo.fileName);
      if (guess && !$('#capName').value) $('#capName').value = guess;
      if (foodGuess) $('#capCat').value = guessPantryCat(foodGuess.base);
      updateCheaper();
      toast('Foto cargada ✓');
    });

    // name input -> live price recommendations
    $('#capName').addEventListener('input', updateCheaper);
    $('#capPrice').addEventListener('input', updateCheaper);

    // target change adjusts fields (meal hides price relevance? keep simple)
    $('#capTarget').addEventListener('change', (e) => {
      capTarget = e.target.value;
      $('#expiryField').style.display = capTarget === 'pantry' ? 'flex' : 'none';
      $('#captureTitle').textContent = capTitles[capTarget];
    });

    $('#saveCap').addEventListener('click', saveCapture);
    $('#captureDialog').addEventListener('close', () => {
      FoodaraCapture.stopScan().then(() => FoodaraCapture.releaseStream());
    });
  }

  function guessPantryCat(base) {
    const n = (base || '').toLowerCase();
    if (/láct|leche|queso|yogur|manteca/.test(n)) return 'Lácteos';
    if (/carne|pollo|cerdo|vac|chorizo/.test(n)) return 'Carnes';
    if (/fruta|banana|manzana|naranja|pera/.test(n)) return 'Frutas';
    if (/verdura|tomate|cebolla|papa|zanahoria|lechuga|verde/.test(n)) return 'Verduras';
    if (/agua|gaseosa|jugo|cerveza|vino|bebida/.test(n)) return 'Bebidas';
    if (/fideo|arroz|harina|azúcar|azucar|sal|aceite|lata|atún|atun|galletita/.test(n)) return 'Almacén';
    if (/congelad|pizza|helado/.test(n)) return 'Congelados';
    return 'Otros';
  }

  /* ================= INIT ================= */
  function init() {
    try { apiUrl = localStorage.getItem('foodara_api') || ''; } catch(e){}
    bindNav();
    initAuth();
    initPantry();
    initPurchases();
    initCapture();
    initAI();
    initProfile();
    document.querySelectorAll('dialog').forEach(d => d.addEventListener('click', (e) => {
      if (e.target === d) d.close();
    }));
  }

  document.addEventListener('DOMContentLoaded', init);
  return { user, go, openCapture };
})();
