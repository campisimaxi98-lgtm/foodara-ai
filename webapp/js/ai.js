/* FOODARA AI - Assistant that uses the real app data */

const FoodaraAI = (() => {
  const daysLeft = (dateStr) => {
    if (!dateStr) return null;
    const exp = new Date(dateStr + 'T23:59:59');
    const today = new Date(); today.setHours(23,59,59,0);
    return Math.ceil((exp - today) / (1000 * 3600 * 24));
  };

  function buildContext() {
    const db = Store.getDB();
    const today = new Date().toISOString().slice(0,10);
    const mealsToday = db.meals.filter(m => m.date === today);
    const cal = mealsToday.reduce((s, m) => s + (+m.cal || 0), 0);
    const prot = mealsToday.reduce((s, m) => s + (+m.prot || 0), 0);
    const expiring = db.pantry
      .map(p => ({ ...p, left: daysLeft(p.expiry) }))
      .filter(p => p.left !== null && p.left <= 3)
      .sort((a, b) => a.left - b.left);

    const thisMonth = today.slice(0,7);
    const totalMonth = db.purchases
      .filter(p => (p.date || '').slice(0,7) === thisMonth)
      .reduce((s, p) => s + (+p.total || 0), 0);

    return { db, today, mealsToday, cal, prot, expiring, totalMonth };
  }

  const fmt = (n) => '$' + Math.round(n).toLocaleString('es-AR');

  function respond(raw) {
    const q = (raw || '').toLowerCase();
    const c = buildContext();
    const { db, mealsToday, cal, prot, expiring, totalMonth, today } = c;

    const js = (html) => ({ html });

    /* ---- Expiring ---- */
    if (/(vencer|vencido|vencimiento|caduc|despensa|proximo)/.test(q) && /(vencer|vencido|caduc)/.test(q)) {
      if (expiring.length === 0) {
        return js('Nada en tu despensa está por vencer. 🎉 Todo al día.');
      }
      let rows = '<table><tr><th>Alimento</th><th>Cant.</th><th>Días</th></tr>';
      expiring.forEach(p => {
        const cls = p.left < 0 ? 'style="color:#ff647c"' : (p.left === 0 ? 'style="color:#ffc85b"' : '');
        rows += `<tr><td>${p.name}</td><td>${p.qty} ${p.unit}</td><td ${cls}>${p.left < 0 ? 'VENCIDO' : (p.left === 0 ? 'Vence hoy' : p.left + 'd')}</td></tr>`;
      });
      rows += '</table>';
      const tip = expiring.find(p => p.left >= 0) ? '<br>Te sugiero usar estos alimentos en tus próximas comidas para evitar desperdicio. 💚' : '';
      return js(`Tenés <b>${expiring.length}</b> producto(s) cerca de vencer:${rows}${tip}`);
    }

    /* ---- Pantry summary ---- */
    if (/(qué tengo|que tengo|qué hay|que hay|cómo está mi despensa|como esta mi despensa|lista).*(despensa|alimento|producto|cuen|pantry|items)/.test(q) &&
        !/(vencer|vencido)/.test(q)) {
      if (db.pantry.length === 0) return js('Tu despensa está vacía. Agregá alimentos desde la sección <b>Despensa</b>. 🥫');
      const cats = {};
      db.pantry.forEach(p => { cats[p.cat] = (cats[p.cat] || 0) + 1; });
      let list = '<ul>';
      Object.entries(cats).sort((a,b) => b[1]-a[1]).forEach(([cat, n]) => list += `<li><b>${cat}</b>: ${n} item(s)</li>`);
      list += '</ul>';
      return js(`Tu despensa tiene <b>${db.pantry.length}</b> items:${list}`);
    }

    /* ---- Spending ---- */
    if (/(gasto|cuanto gaste|cuánto gast|compras|gasté|gaste en)/.test(q)) {
      const count = db.purchases.length;
      if (count === 0) return js('Todavía no registraste compras. Cuando lo hagas te muestro tu evolución de gastos. 🛒');
      const avg = totalMonth / (db.purchases.filter(p => (p.date||'').slice(0,7) === today.slice(0,7)).length || 1);
      let html = `Este mes gastaste <b>${fmt(totalMonth)}</b> en ${db.purchases.filter(p=>(p.date||'').slice(0,7)===today.slice(0,7)).length} compra(s).`;
      html += `<br>Gasto promedio por compra: <b>${fmt(avg)}</b>.`;
      return js(html);
    }

    /* ---- Calories / nutrition ---- */
    if (/(calor|nutric|macro|prote|comí|comi|registré|registre)/.test(q)) {
      const g = db.goals;
      const pct = (c, g) => Math.min(100, Math.round((c / g) * 100));
      if (mealsToday.length === 0) {
        return js('Hoy todavía no registraste comidas. Registrá lo que comés y te muestro tu nutrición del día. 🍽️');
      }
      return js(`Hoy consumiste <b>${cal} kcal</b> (${pct(cal, g.cal)}% de tu meta de ${g.cal} kcal).<br>` +
                `Proteínas: <b>${Math.round(prot)}g</b> / ${g.prot}g.<br>` +
                `Registraste <b>${mealsToday.length}</b> comida(s) hoy.`);
    }

    /* ---- Waste ---- */
    if (/(desperdicio|desperdici|eficien|ahorro|ahorr)/.test(q)) {
      const wasted = db.pantry.filter(p => daysLeft(p.expiry) !== null && daysLeft(p.expiry) < 0).length;
      const avoid = db.pantry.length ? Math.round((expiring.filter(e=>e.left>=0).length / db.pantry.length) * 100) : 0;
      if (wasted === 0) return js(`Estás evitando desperdicio muy bien: solo <b>${avoid}%</b> de tu despensa está por vencer y nada está vencido. 💚`);
      return js(`Tenés <b>${wasted}</b> item(s) ya vencidos y <b>${expiring.filter(e=>e.left>=0).length}</b> por vencer. Revisá la despensa para reorganizar. ♻️`);
    }

    /* ---- Suggestions ---- */
    if (/(suger|recomend|consejo|qué hago|que hago|ayuda)/.test(q)) {
      let tips = ['Planificá la semana con lo que ya tenés en la despensa para no comprar de más.'];
      if (expiring.length) tips.push(`Usá productos por vencer como <b>${expiring[0].name}</b> en tu próxima comida.`);
      if (db.pantry.length > 30) tips.push('Tu despensa está muy llena. Revisá fechas de vencimiento antes de comprar más.');
      tips.push('Registrá cada compra para que FOODARA calcule tu ahorro estimado.');
      return js('<b>Mis sugerencias:</b><ul>' + tips.map(t => `<li>${t}</li>`).join('') + '</ul>');
    }

    /* ---- Greeting ---- */
    if (/(hola|buenas|hey|que tal|qué tal|como estas|cómo estás)/.test(q)) {
      return js(`¡Hola ${app.user?.name || ''}! 👋 Te resumo: tenés <b>${db.pantry.length}</b> items en la despensa${expiring.length ? ` y <b>${expiring.length}</b> por vencer` : ''}. ¿En qué te ayudo?`);
    }

    /* ---- help ---- */
    if (/(que podes|qué podés|que sabes|qué sabés|funciones|help|ayuda)/.test(q)) {
      return js('Puedo ayudarte con:<ul><li>📋 <b>Qué tengo en la despensa</b> (ej: "¿qué tengo?")</li><li>⏳ <b>Productos por vencer</b> (ej: "¿qué vence pronto?")</li><li>🛒 <b>Tus gastos</b> (ej: "¿cuánto gasté este mes?")</li><li>🥗 <b>Tu nutrición del día</b> (ej: "¿cuántas calorías comí?")</li><li>♻️ <b>Desperdicio</b> y consejos</li></ul>');
    }

    /* ---- default ---- */
    return js('Buena pregunta. Puedo decirte qué tenés en la despensa, qué está por vencer, cuánto gastaste o tu nutrición del día. Probá con: <i>"¿qué tengo por vencer?"</i>');
  }

  return { respond };
})();
