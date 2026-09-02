/* FOODARA - Data store (localStorage with optional API sync) */

const Store = (() => {
  const DB_KEY = 'foodara_db_v1';
  const USER_KEY = 'foodara_user_v1';

  const emptyDB = () => ({
    users: [],
    pantry: [],      // {id, name, qty, unit, expiry, cat, price, added}
    purchases: [],   // {id, store, date, items:[{name,qty,price}], total}
    meals: [],       // {id, date, name, cal, prot, carb, fat}
    goals: { cal: 2000, prot: 128, carb: 225, fat: 80 }
  });

  function load() {
    try {
      const raw = localStorage.getItem(DB_KEY);
      const db = raw ? JSON.parse(raw) : null;
      if (db && db.pantry && db.purchases && db.meals) return db;
    } catch (e) { /* corrupt */ }
    const db = emptyDB();
    save(db);
    return db;
  }

  function save(db) {
    try { localStorage.setItem(DB_KEY, JSON.stringify(db)); } catch (e) {}
  }

  function getDB() { return load(); }
  function reset() { const db = emptyDB(); save(db); return db; }
  function commit(mutator) {
    const db = load();
    mutator(db);
    save(db);
    return db;
  }

  function getSession() {
    try { return JSON.parse(localStorage.getItem(USER_KEY)); } catch (e) { return null; }
  }
  function setSession(u) {
    if (u) localStorage.setItem(USER_KEY, JSON.stringify(u));
    else localStorage.removeItem(USER_KEY);
  }

  /* Auth */
  function register(name, email, pass) {
    const db = load();
    if (db.users.some(u => u.email.toLowerCase() === email.toLowerCase())) {
      return { error: 'Ya existe una cuenta con ese email. Iniciá sesión.' };
    }
    const user = { id: 'u' + Date.now(), name, email, pass };
    db.users.push(user);
    save(db);
    return { user };
  }

  function login(email, pass) {
    const db = load();
    const user = db.users.find(u => u.email.toLowerCase() === email.toLowerCase());
    if (!user) return { error: 'No encontramos esa cuenta. Creala primero.' };
    if (user.pass !== pass) return { error: 'Contraseña incorrecta.' };
    return { user };
  }

  const uid = () => 'i' + Date.now() + Math.floor(Math.random() * 999);

  return {
    uid, commit, reset, getDB, getSession, setSession, register, login
  };
})();
