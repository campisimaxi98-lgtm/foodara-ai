/* FOODARA - Cheaper product recommendations */

const PriceFinder = (() => {
  // Curated Argentine supermarket price reference (ARS, June 2026 typical prices).
  // keyed by normalized product name -> list of brand/price/store alternatives.
  const DB = [
    { name: 'leche', base: 'Leche entera', options: [
      { label: 'La Serenísima 1L', price: 1499 }, { label: 'Milkaut 1L', price: 1450 }, { label: 'Verónica 1L', price: 1385 } ] },
    { name: 'yogur', base: 'Yogur', options: [
      { label: 'La Serenísima 190g', price: 950 }, { label: 'Sancor 190g', price: 880 }, { label: 'Toddy 190g', price: 790 } ] },
    { name: 'yogurt', base: 'Yogur', options: [
      { label: 'La Serenísima 190g', price: 950 }, { label: 'Sancor 190g', price: 880 }, { label: 'Toddy 190g', price: 790 } ] },
    { name: 'queso', base: 'Queso', options: [
      { label: 'Sancor Cremoso 1kg', price: 8999 }, { label: 'La Serenísima Cremoso 1kg', price: 9250 }, { label: 'Ilolay 1kg', price: 8700 } ] },
    { name: 'pan', base: 'Pan', options: [
      { label: 'Pan de molde Fargo 560g', price: 2199 }, { label: 'Lacnor 560g', price: 1999 }, { label: 'Bimbo Blanco 600g', price: 2399 } ] },
    { name: 'harina', base: 'Harina', options: [
      { label: 'Harina 0000 Cañuelas 1kg', price: 1399 }, { label: 'Morixe 1kg', price: 1290 }, { label: 'Cóndor 1kg', price: 1250 } ] },
    { name: 'arroz', base: 'Arroz', options: [
      { label: 'Gallo Oro 1kg', price: 2599 }, { label: 'Alicante 1kg', price: 2490 }, { label: 'Marolio 1kg', price: 2149 } ] },
    { name: 'fideo', base: 'Fideos', options: [
      { label: 'Matarazzo Spaghetti 500g', price: 1499 }, { label: 'Marolio 500g', price: 1290 }, { label: 'Suave 500g (2da marca)', price: 990 } ] },
    { name: 'fideos', base: 'Fideos', options: [
      { label: 'Matarazzo Spaghetti 500g', price: 1499 }, { label: 'Marolio 500g', price: 1290 }, { label: 'Suave 500g (2da marca)', price: 990 } ] },
    { name: 'aceite', base: 'Aceite', options: [
      { label: 'Natura 900ml', price: 3999 }, { label: 'Cocinero 900ml', price: 4250 }, { label: 'Marca propia 900ml', price: 3490 } ] },
    { name: 'azucar', base: 'Azúcar', options: [
      { label: 'Ledesma 1kg', price: 1799 }, { label: 'Chango 1kg', price: 1690 }, { label: 'Marolio 1kg', price: 1490 } ] },
    { name: 'azúcar', base: 'Azúcar', options: [
      { label: 'Ledesma 1kg', price: 1799 }, { label: 'Chango 1kg', price: 1690 }, { label: 'Marolio 1kg', price: 1490 } ] },
    { name: 'sal', base: 'Sal', options: [
      { label: 'Celusal 500g', price: 699 }, { label: 'Dos Anclas 500g', price: 740 }, { label: 'Marca propia 500g', price: 550 } ] },
    { name: 'cafe', base: 'Café', options: [
      { label: 'Cabrales 500g', price: 7999 }, { label: 'La Virginia 500g', price: 7590 }, { label: 'Dos Águilas 500g', price: 7200 } ] },
    { name: 'café', base: 'Café', options: [
      { label: 'Cabrales 500g', price: 7999 }, { label: 'La Virginia 500g', price: 7590 }, { label: 'Dos Águilas 500g', price: 7200 } ] },
    { name: 'te', base: 'Té', options: [
      { label: 'Taragüi 25 saquitos', price: 1999 }, { label: 'La Virginia 25', price: 2100 }, { label: 'Chamigo 25 (2da)', price: 1690 } ] },
    { name: 'té', base: 'Té', options: [
      { label: 'Taragüi 25 saquitos', price: 1999 }, { label: 'La Virginia 25', price: 2100 }, { label: 'Chamigo 25 (2da)', price: 1690 } ] },
    { name: 'carne', base: 'Carne', options: [
      { label: 'Carne picada común', price: 7990 }, { label: 'Nalga 1kg', price: 9890 }, { label: 'Oferta carnicería barrial', price: 7490 } ] },
    { name: 'pollo', base: 'Pollo', options: [
      { label: 'Pollo entero', price: 5990 }, { label: 'Pata y muslo 1kg', price: 4590 }, { label: 'Pechuga 1kg', price: 8690 } ] },
    { name: 'huevo', base: 'Huevos', options: [
      { label: 'Media docena', price: 1450 }, { label: 'Docena', price: 2850 }, { label: 'Maple (30)', price: 6990 } ] },
    { name: 'huevos', base: 'Huevos', options: [
      { label: 'Media docena', price: 1450 }, { label: 'Docena', price: 2850 }, { label: 'Maple (30)', price: 6990 } ] },
    { name: 'tomate', base: 'Tomate', options: [
      { label: 'Tomate perita 1kg', price: 2890 }, { label: 'Lata 400g', price: 1499 }, { label: 'En conserva Marolio 400g', price: 1290 } ] },
    { name: 'tomates', base: 'Tomate', options: [
      { label: 'Tomate perita 1kg', price: 2890 }, { label: 'Lata 400g', price: 1499 }, { label: 'En conserva Marolio 400g', price: 1290 } ] },
    { name: 'banana', base: 'Banana', options: [
      { label: 'Banana 1kg', price: 1650 }, { label: 'Banana manzana 1kg', price: 1850 } ] },
    { name: 'manzana', base: 'Manzana', options: [
      { label: 'Manzana roja 1kg', price: 2290 }, { label: 'Manzana verde 1kg', price: 2150 }, { label: 'Manzana (2da) 1kg', price: 1890 } ] },
    { name: 'papa', base: 'Papa', options: [
      { label: 'Papa 1kg', price: 1390 }, { label: 'Bolsa 5kg', price: 5990 } ] },
    { name: 'papas', base: 'Papa', options: [
      { label: 'Papa 1kg', price: 1390 }, { label: 'Bolsa 5kg', price: 5990 } ] },
    { name: 'zanahoria', base: 'Zanahoria', options: [
      { label: 'Zanahoria 1kg', price: 990 }, { label: 'Bolsa 3kg', price: 2690 } ] },
    { name: 'cebolla', base: 'Cebolla', options: [
      { label: 'Cebolla 1kg', price: 1290 }, { label: 'Bolsa 3kg', price: 3490 } ] },
    { name: 'atun', base: 'Atún', options: [
      { label: 'Gómez 170g', price: 2490 }, { label: 'La Campagnola 170g', price: 2350 }, { label: 'Marca propia 170g', price: 1990 } ] },
    { name: 'atún', base: 'Atún', options: [
      { label: 'Gómez 170g', price: 2490 }, { label: 'La Campagnola 170g', price: 2350 }, { label: 'Marca propia 170g', price: 1990 } ] },
    { name: 'galletita', base: 'Galletitas', options: [
      { label: 'Surtido Bagley', price: 1799 }, { label: 'Bagley (2da) 400g', price: 1390 }, { label: 'Marca propia 400g', price: 1190 } ] },
    { name: 'galletitas', base: 'Galletitas', options: [
      { label: 'Surtido Bagley', price: 1799 }, { label: 'Bagley (2da) 400g', price: 1390 }, { label: 'Marca propia 400g', price: 1190 } ] },
    { name: 'agua', base: 'Agua mineral', options: [
      { label: 'Villavicencio 2.25L', price: 2399 }, { label: 'Eco de los Andes 2.25L', price: 2490 }, { label: 'Agua de mesa 2L (marca propia)', price: 1290 } ] },
    { name: 'gaseosa', base: 'Gaseosa', options: [
      { label: 'Coca-Cola 2.25L', price: 3499 }, { label: 'Pepsi 2.25L', price: 3190 }, { label: 'Manaos 2.25L', price: 1690 } ] },
    { name: 'cerveza', base: 'Cerveza', options: [
      { label: 'Quilmes 1L', price: 2699 }, { label: 'Patagonia 473ml', price: 1990 }, { label: 'Andes 473ml', price: 1850 } ] },
    { name: 'jugo', base: 'Jugo', options: [
      { label: 'Cepita 1L', price: 2290 }, { label: 'Baggio 1L', price: 1990 }, { label: 'Marca propia 1L', price: 1490 } ] }
  ];

  // Suggested smart tips (based on typical savings behaviors)
  const TIPS = [
    'Comprá las segundas marcas: suelen costar hasta 30% menos por el mismo producto.',
    'Verduras y frutas por kilo en verdulería suelen ser más baratas que en bandejas de super.',
    'Compará el precio por unidad, no por presentación: la bolsa de 5kg casi siempre conviene.',
    'Los productos de marca propia del supermercado suelen ser 20-40% más baratos.',
    'Compra el jueves y domingo a la tarde: muchas ofertas de carnes y lácteos se descuentan.'
  ];

  function normalize(s) {
    return String(s || '').toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')  // remove accents
      .replace(/[^a-z0-9]+/g, ' ').trim();
  }

  // find the closest DB entry for a product name
  function match(name) {
    const n = normalize(name);
    if (!n) return null;
    // exact or contains match on the name key
    for (const e of DB) {
      if (e.name === n || n === e.name) return e;
    }
    // substring: product "arroz gallo" contains "arroz"
    for (const e of DB) {
      if (n.includes(e.name) || e.name.includes(n)) return e;
    }
    return null;
  }

  // Given a product name and optional budget, return recommendations sorted by savings
  function findCheaper(name, currentPrice) {
    const e = match(name);
    if (!e) {
      // no reference -> still give generic tip + a manual suggestion
      return { found: false, base: name, options: [], savingsPct: null, totalAnnual: null };
    }
    const current = currentPrice && currentPrice > 0 ? currentPrice : null;
    const options = e.options.map(o => {
      const diff = current ? current - o.price : null;
      const pct = diff && diff > 0 ? Math.round((diff / current) * 100) : 0;
      return { ...o, diff, pct };
    });
    // sort: if current price known, most saving first (or cheapest first)
    options.sort((a, b) => (b.diff || b.price) - (a.diff || a.price));

    // estimate annual savings (4x/month)
    const best = current ? Math.max(...options.map(o => o.diff || 0)) : null;
    const totalAnnual = best ? Math.round(best * 4 * 12) : null;

    return {
      found: true,
      base: e.base,
      options,
      current,
      best,
      totalAnnual,
      tip: TIPS[Math.floor(Math.random() * TIPS.length)]
    };
  }

  // returns a random relevant tip for a given product
  function tipFor(name) {
    const e = match(name);
    if (e) return e.tip || TIPS[0];
    return TIPS[Math.floor(Math.random() * TIPS.length)];
  }

  return { findCheaper, match, tipFor };
})();
