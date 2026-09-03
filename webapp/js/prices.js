/* FOODARA - Cheaper product recommendations.
   Catálogo referencial offline (precios ARS típicos 2026).
   Cada producto compara la MISMA referencia entre marcas/presentaciones
   para recomendar la opción más barata. Incluye calorías (kcal) por unidad.
   Para datos reales de códigos de barras se usa Open Food Facts (scanner.js). */

const PriceFinder = (() => {
  // name: clave normalizada · base: nombre visible · cat: categoría · kcal: calorías ref.
  // options: alternativas del MISMO producto (marca/presentación) con precio.
  const DB = [
    /* ================= LÁCTEOS ================= */
    { name: 'leche', base: 'Leche entera', cat: 'Lácteos', kcal: 62, options: [
      { label: 'La Serenísima 1L', price: 1499 }, { label: 'Milkaut 1L', price: 1450 }, { label: 'Verónica 1L', price: 1385 } ] },
    { name: 'leche descremada', base: 'Leche descremada', cat: 'Lácteos', kcal: 35, options: [
      { label: 'La Serenísima 1L', price: 1499 }, { label: 'Milkaut 1L', price: 1440 } ] },
    { name: 'yogur', base: 'Yogur', cat: 'Lácteos', kcal: 85, options: [
      { label: 'La Serenísima 190g', price: 950 }, { label: 'Sancor 190g', price: 880 }, { label: 'Toddy 190g', price: 790 } ] },
    { name: 'yogurt', base: 'Yogur', cat: 'Lácteos', kcal: 85, options: [
      { label: 'La Serenísima 190g', price: 950 }, { label: 'Sancor 190g', price: 880 }, { label: 'Toddy 190g', price: 790 } ] },
    { name: 'queso', base: 'Queso cremoso', cat: 'Lácteos', kcal: 350, options: [
      { label: 'Sancor Cremoso 1kg', price: 8999 }, { label: 'La Serenísima Cremoso 1kg', price: 9250 }, { label: 'Ilolay 1kg', price: 8700 } ] },
    { name: 'queso rallado', base: 'Queso rallado', cat: 'Lácteos', kcal: 400, options: [
      { label: 'Sancor 120g', price: 1899 }, { label: 'La Serenísima 120g', price: 1950 }, { label: 'Marca propia 120g', price: 1490 } ] },
    { name: 'manteca', base: 'Manteca', cat: 'Lácteos', kcal: 750, options: [
      { label: 'La Serenísima 200g', price: 2199 }, { label: 'Sancor 200g', price: 2090 }, { label: 'Marca propia 200g', price: 1750 } ] },
    { name: 'margarina', base: 'Margarina', cat: 'Lácteos', kcal: 700, options: [
      { label: 'Dánica 200g', price: 1699 }, { label: 'Marca propia 200g', price: 1250 } ] },
    { name: 'crema', base: 'Crema de leche', cat: 'Lácteos', kcal: 280, options: [
      { label: 'Serenísima 200g', price: 1599 }, { label: 'Tregar 200g', price: 1390 }, { label: 'Marca propia 200g', price: 1190 } ] },
    { name: 'dulce de leche', base: 'Dulce de leche', cat: 'Lácteos', kcal: 310, options: [
      { label: 'La Serenísima 400g', price: 1999 }, { label: 'Sancor 400g', price: 1890 }, { label: 'Marca propia 400g', price: 1490 } ] },
    { name: 'florida', base: 'Queso en hebras (muzza)', cat: 'Lácteos', kcal: 350, options: [
      { label: 'Sancor Hebras 250g', price: 2599 }, { label: 'Marca propia 250g', price: 1990 } ] },

    /* ================= CARNES / PESCADOS ================= */
    { name: 'carne', base: 'Carne', cat: 'Carnes', kcal: 250, options: [
      { label: 'Carne picada común', price: 7990 }, { label: 'Nalga 1kg', price: 9890 }, { label: 'Oferta carnicería barrial', price: 7490 } ] },
    { name: 'nalga', base: 'Nalga', cat: 'Carnes', kcal: 210, options: [
      { label: 'Nalga 1kg super', price: 9890 }, { label: 'Nalga carnicería', price: 9290 } ] },
    { name: 'asado', base: 'Asado (tira)', cat: 'Carnes', kcal: 320, options: [
      { label: 'Asado 1kg', price: 8990 }, { label: 'Oferta fin de semana', price: 7890 } ] },
    { name: 'vacio', base: 'Vacío', cat: 'Carnes', kcal: 290, options: [
      { label: 'Vacío 1kg', price: 10590 }, { label: 'Vacío oferta', price: 9490 } ] },
    { name: 'picada', base: 'Carne picada', cat: 'Carnes', kcal: 260, options: [
      { label: 'Picada común 1kg', price: 7990 }, { label: 'Picada especial 1kg', price: 8990 } ] },
    { name: 'pollo', base: 'Pollo', cat: 'Carnes', kcal: 175, options: [
      { label: 'Pollo entero', price: 5990 }, { label: 'Pata y muslo 1kg', price: 4590 }, { label: 'Pechuga 1kg', price: 8690 } ] },
    { name: 'pechuga', base: 'Pechuga de pollo', cat: 'Carnes', kcal: 165, options: [
      { label: 'Pechuga 1kg', price: 8690 }, { label: 'Suprema congelada 1kg', price: 7490 } ] },
    { name: 'atun', base: 'Atún', cat: 'Almacén', kcal: 198, options: [
      { label: 'Gómez 170g', price: 2490 }, { label: 'La Campagnola 170g', price: 2350 }, { label: 'Marca propia 170g', price: 1990 } ] },
    { name: 'atún', base: 'Atún', cat: 'Almacén', kcal: 198, options: [
      { label: 'Gómez 170g', price: 2490 }, { label: 'La Campagnola 170g', price: 2350 }, { label: 'Marca propia 170g', price: 1990 } ] },
    { name: 'caballa', base: 'Caballa en lata', cat: 'Almacén', kcal: 205, options: [
      { label: 'Gómez 170g', price: 1990 }, { label: 'Marca propia 170g', price: 1490 } ] },
    { name: 'cerdo', base: 'Cerdo (bondiola)', cat: 'Carnes', kcal: 280, options: [
      { label: 'Bondiola 1kg', price: 7990 }, { label: 'Oferta cerdo', price: 6990 } ] },
    { name: 'hamburguesa', base: 'Hamburguesas', cat: 'Congelados', kcal: 260, options: [
      { label: 'Paty 4u', price: 3999 }, { label: 'Granja de Oro 4u', price: 3490 }, { label: 'Marca propia 4u', price: 2890 } ] },
    { name: 'milanesa', base: 'Milanesas', cat: 'Congelados', kcal: 300, options: [
      { label: 'Navillén 1kg', price: 8999 }, { label: 'Marca propia 1kg', price: 7490 } ] },

    /* ================= ALMACÉN ================= */
    { name: 'pan', base: 'Pan de molde', cat: 'Panadería', kcal: 265, options: [
      { label: 'Pan de molde Fargo 560g', price: 2199 }, { label: 'Lacnor 560g', price: 1999 }, { label: 'Bimbo Blanco 600g', price: 2399 } ] },
    { name: 'harina', base: 'Harina', cat: 'Almacén', kcal: 360, options: [
      { label: 'Harina 0000 Cañuelas 1kg', price: 1399 }, { label: 'Morixe 1kg', price: 1290 }, { label: 'Cóndor 1kg', price: 1250 } ] },
    { name: 'harina integral', base: 'Harina integral', cat: 'Almacén', kcal: 330, options: [
      { label: 'Cañuelas integral 1kg', price: 1499 }, { label: 'Marca propia 1kg', price: 1290 } ] },
    { name: 'arroz', base: 'Arroz', cat: 'Almacén', kcal: 360, options: [
      { label: 'Gallo Oro 1kg', price: 2599 }, { label: 'Alicante 1kg', price: 2490 }, { label: 'Marolio 1kg', price: 2149 } ] },
    { name: 'arroz integral', base: 'Arroz integral', cat: 'Almacén', kcal: 340, options: [
      { label: 'Gallo 1kg', price: 2899 }, { label: 'Marca propia 1kg', price: 2390 } ] },
    { name: 'fideo', base: 'Fideos', cat: 'Almacén', kcal: 350, options: [
      { label: 'Matarazzo Spaghetti 500g', price: 1499 }, { label: 'Marolio 500g', price: 1290 }, { label: 'Suave 500g (2da marca)', price: 990 } ] },
    { name: 'fideos', base: 'Fideos', cat: 'Almacén', kcal: 350, options: [
      { label: 'Matarazzo Spaghetti 500g', price: 1499 }, { label: 'Marolio 500g', price: 1290 }, { label: 'Suave 500g (2da marca)', price: 990 } ] },
    { name: 'spaghetti', base: 'Fideos spaghetti', cat: 'Almacén', kcal: 350, options: [
      { label: 'Luchetti 500g', price: 1699 }, { label: 'Marolio 500g', price: 1290 }, { label: 'Suave 500g', price: 990 } ] },
    { name: 'typo', base: 'Fideos tirabuzón', cat: 'Almacén', kcal: 350, options: [
      { label: 'Matarazzo 500g', price: 1499 }, { label: 'Marolio 500g', price: 1290 } ] },
    { name: 'aceite', base: 'Aceite', cat: 'Almacén', kcal: 900, options: [
      { label: 'Natura 900ml', price: 3999 }, { label: 'Cocinero 900ml', price: 4250 }, { label: 'Marca propia 900ml', price: 3490 } ] },
    { name: 'aceite oliva', base: 'Aceite de oliva', cat: 'Almacén', kcal: 880, options: [
      { label: 'Nucete 500ml', price: 4999 }, { label: 'Marca propia 500ml', price: 3890 } ] },
    { name: 'azucar', base: 'Azúcar', cat: 'Almacén', kcal: 380, options: [
      { label: 'Ledesma 1kg', price: 1799 }, { label: 'Chango 1kg', price: 1690 }, { label: 'Marolio 1kg', price: 1490 } ] },
    { name: 'azúcar', base: 'Azúcar', cat: 'Almacén', kcal: 380, options: [
      { label: 'Ledesma 1kg', price: 1799 }, { label: 'Chango 1kg', price: 1690 }, { label: 'Marolio 1kg', price: 1490 } ] },
    { name: 'edulcorante', base: 'Edulcorante', cat: 'Almacén', kcal: 5, options: [
      { label: 'Hileret 120ml', price: 1699 }, { label: 'Marca propia 120ml', price: 1190 } ] },
    { name: 'sal', base: 'Sal', cat: 'Almacén', kcal: 0, options: [
      { label: 'Celusal 500g', price: 699 }, { label: 'Dos Anclas 500g', price: 740 }, { label: 'Marca propia 500g', price: 550 } ] },
    { name: 'cafe', base: 'Café', cat: 'Almacén', kcal: 2, options: [
      { label: 'Cabrales 500g', price: 7999 }, { label: 'La Virginia 500g', price: 7590 }, { label: 'Dos Águilas 500g', price: 7200 } ] },
    { name: 'café', base: 'Café', cat: 'Almacén', kcal: 2, options: [
      { label: 'Cabrales 500g', price: 7999 }, { label: 'La Virginia 500g', price: 7590 }, { label: 'Dos Águilas 500g', price: 7200 } ] },
    { name: 'te', base: 'Té', cat: 'Almacén', kcal: 1, options: [
      { label: 'Taragüi 25 saquitos', price: 1999 }, { label: 'La Virginia 25', price: 2100 }, { label: 'Chamigo 25 (2da)', price: 1690 } ] },
    { name: 'té', base: 'Té', cat: 'Almacén', kcal: 1, options: [
      { label: 'Taragüi 25 saquitos', price: 1999 }, { label: 'La Virginia 25', price: 2100 }, { label: 'Chamigo 25 (2da)', price: 1690 } ] },
    { name: 'yerba', base: 'Yerba mate', cat: 'Almacén', kcal: 35, options: [
      { label: 'Playadito 1kg', price: 4999 }, { label: 'Taragüi 1kg', price: 4790 }, { label: 'Mañanita 1kg', price: 3890 } ] },
    { name: 'galletita', base: 'Galletitas', cat: 'Almacén', kcal: 480, options: [
      { label: 'Surtido Bagley', price: 1799 }, { label: 'Bagley (2da) 400g', price: 1390 }, { label: 'Marca propia 400g', price: 1190 } ] },
    { name: 'galletitas', base: 'Galletitas', cat: 'Almacén', kcal: 480, options: [
      { label: 'Surtido Bagley', price: 1799 }, { label: 'Bagley (2da) 400g', price: 1390 }, { label: 'Marca propia 400g', price: 1190 } ] },
    { name: 'cereal', base: 'Cereal', cat: 'Almacén', kcal: 380, options: [
      { label: 'Granix 300g', price: 2499 }, { label: 'Marca propia 300g', price: 1890 } ] },
    { name: 'avena', base: 'Avena', cat: 'Almacén', kcal: 370, options: [
      { label: 'Quaker 500g', price: 1999 }, { label: 'Granix 500g', price: 1790 }, { label: 'Marca propia 500g', price: 1390 } ] },
    { name: 'maiz', base: 'Maíz', cat: 'Almacén', kcal: 360, options: [
      { label: 'Gallo 500g', price: 1799 }, { label: 'Marca propia 500g', price: 1290 } ] },
    { name: 'lenteja', base: 'Lentejas', cat: 'Almacén', kcal: 330, options: [
      { label: 'Noel 500g', price: 1999 }, { label: 'Marca propia 500g', price: 1490 } ] },
    { name: 'lentejas', base: 'Lentejas', cat: 'Almacén', kcal: 330, options: [
      { label: 'Noel 500g', price: 1999 }, { label: 'Marca propia 500g', price: 1490 } ] },
    { name: 'garbanzo', base: 'Garbanzos', cat: 'Almacén', kcal: 330, options: [
      { label: 'Noel 500g', price: 2199 }, { label: 'Marca propia 500g', price: 1590 } ] },
    { name: 'garbanzos', base: 'Garbanzos', cat: 'Almacén', kcal: 330, options: [
      { label: 'Noel 500g', price: 2199 }, { label: 'Marca propia 500g', price: 1590 } ] },
    { name: 'poroto', base: 'Porotos', cat: 'Almacén', kcal: 340, options: [
      { label: 'Noel 500g', price: 2199 }, { label: 'Marca propia 500g', price: 1590 } ] },
    { name: 'porotos', base: 'Porotos', cat: 'Almacén', kcal: 340, options: [
      { label: 'Noel 500g', price: 2199 }, { label: 'Marca propia 500g', price: 1590 } ] },
    { name: 'mayonesa', base: 'Mayonesa', cat: 'Almacén', kcal: 700, options: [
      { label: 'Hellmann\'s 500g', price: 2799 }, { label: 'Natura 500g', price: 2290 }, { label: 'Marca propia 500g', price: 1690 } ] },
    { name: 'ketchup', base: 'Ketchup', cat: 'Almacén', kcal: 110, options: [
      { label: 'Hellmann\'s 340g', price: 1799 }, { label: 'Marca propia 340g', price: 1190 } ] },
    { name: 'mostaza', base: 'Mostaza', cat: 'Almacén', kcal: 70, options: [
      { label: 'Savora 250g', price: 1299 }, { label: 'Marca propia 250g', price: 890 } ] },
    { name: 'mermelada', base: 'Mermelada', cat: 'Almacén', kcal: 250, options: [
      { label: 'Arcor 454g', price: 1899 }, { label: 'La Campagnola 454g', price: 1790 }, { label: 'Marca propia 454g', price: 1290 } ] },
    { name: 'miel', base: 'Miel', cat: 'Almacén', kcal: 300, options: [
      { label: 'Cabaña Suiza 500g', price: 3499 }, { label: 'Dietética 500g', price: 2690 } ] },
    { name: 'pasta salsa', base: 'Salsa de tomate', cat: 'Almacén', kcal: 40, options: [
      { label: 'Knorr 500g', price: 1599 }, { label: 'Marolio 500g', price: 1190 }, { label: 'Marca propia 500g', price: 890 } ] },
    { name: 'tomate', base: 'Tomate', cat: 'Verduras', kcal: 20, options: [
      { label: 'Tomate perita 1kg', price: 2890 }, { label: 'Lata 400g', price: 1499 }, { label: 'En conserva Marolio 400g', price: 1290 } ] },
    { name: 'tomates', base: 'Tomate', cat: 'Verduras', kcal: 20, options: [
      { label: 'Tomate perita 1kg', price: 2890 }, { label: 'Lata 400g', price: 1499 }, { label: 'En conserva Marolio 400g', price: 1290 } ] },
    { name: 'pure de tomate', base: 'Puré de tomate', cat: 'Almacén', kcal: 45, options: [
      { label: 'Marolio 530g', price: 1299 }, { label: 'Marca propia 530g', price: 990 } ] },
    { name: 'vinagre', base: 'Vinagre', cat: 'Almacén', kcal: 20, options: [
      { label: 'Fama 500ml', price: 699 }, { label: 'Marca propia 500ml', price: 490 } ] },
    { name: 'arroz con leche', base: 'Arroz con leche', cat: 'Almacén', kcal: 150, options: [
      { label: 'Alimenta 170g', price: 1299 }, { label: 'Marca propia 170g', price: 990 } ] },
    { name: 'choclo', base: 'Choclo', cat: 'Almacén', kcal: 130, options: [
      { label: 'Arcor en lata 220g', price: 1599 }, { label: 'Marca propia 220g', price: 1190 } ] },
    { name: 'arvejas', base: 'Arvejas', cat: 'Almacén', kcal: 85, options: [
      { label: 'Arcor 300g', price: 1399 }, { label: 'Marca propia 300g', price: 990 } ] },

    /* ================= VERDURAS ================= */
    { name: 'papa', base: 'Papa', cat: 'Verduras', kcal: 77, options: [
      { label: 'Papa 1kg', price: 1390 }, { label: 'Bolsa 5kg', price: 5990 } ] },
    { name: 'papas', base: 'Papa', cat: 'Verduras', kcal: 77, options: [
      { label: 'Papa 1kg', price: 1390 }, { label: 'Bolsa 5kg', price: 5990 } ] },
    { name: 'zanahoria', base: 'Zanahoria', cat: 'Verduras', kcal: 41, options: [
      { label: 'Zanahoria 1kg', price: 990 }, { label: 'Bolsa 3kg', price: 2690 } ] },
    { name: 'cebolla', base: 'Cebolla', cat: 'Verduras', kcal: 40, options: [
      { label: 'Cebolla 1kg', price: 1290 }, { label: 'Bolsa 3kg', price: 3490 } ] },
    { name: 'lechuga', base: 'Lechuga', cat: 'Verduras', kcal: 15, options: [
      { label: 'Lechuga 1u', price: 1290 }, { label: 'Lechuga en cartera (2u)', price: 1990 } ] },
    { name: 'tomate fresco', base: 'Tomate fresco', cat: 'Verduras', kcal: 20, options: [
      { label: 'Tomate perita 1kg', price: 2890 }, { label: 'Tomate redondo 1kg', price: 2590 } ] },
    { name: 'pimiento', base: 'Pimiento', cat: 'Verduras', kcal: 26, options: [
      { label: 'Pimiento rojo 1kg', price: 3490 }, { label: 'Pimiento verde 1kg', price: 2990 } ] },
    { name: 'morron', base: 'Morrón', cat: 'Verduras', kcal: 26, options: [
      { label: 'Morrón rojo 1kg', price: 3490 }, { label: 'Morrón verde 1kg', price: 2990 } ] },
    { name: 'acelga', base: 'Acelga', cat: 'Verduras', kcal: 19, options: [
      { label: 'Acelga 1 atado', price: 1490 }, { label: 'Espinaca 1 atado', price: 1690 } ] },
    { name: 'brocoli', base: 'Brócoli', cat: 'Verduras', kcal: 34, options: [
      { label: 'Brócoli fresco 1u', price: 2490 }, { label: 'Brócoli congelado 400g', price: 1990 } ] },
    { name: 'brócoli', base: 'Brócoli', cat: 'Verduras', kcal: 34, options: [
      { label: 'Brócoli fresco 1u', price: 2490 }, { label: 'Brócoli congelado 400g', price: 1990 } ] },
    { name: 'zapallo', base: 'Zapallo', cat: 'Verduras', kcal: 26, options: [
      { label: 'Zapallo 1kg', price: 1190 }, { label: 'Zapallo anco 1kg', price: 1390 } ] },
    { name: 'calabacin', base: 'Calabacín', cat: 'Verduras', kcal: 17, options: [
      { label: 'Calabacín 1kg', price: 1890 }, { label: 'Zapallito 1kg', price: 1990 } ] },
    { name: 'espinaca', base: 'Espinaca', cat: 'Verduras', kcal: 23, options: [
      { label: 'Espinaca 1 atado', price: 1690 }, { label: 'Espinaca congelada', price: 1490 } ] },
    { name: 'huevo', base: 'Huevos', cat: 'Verduras', kcal: 78, options: [
      { label: 'Media docena', price: 1450 }, { label: 'Docena', price: 2850 }, { label: 'Maple (30)', price: 6990 } ] },
    { name: 'huevos', base: 'Huevos', cat: 'Verduras', kcal: 78, options: [
      { label: 'Media docena', price: 1450 }, { label: 'Docena', price: 2850 }, { label: 'Maple (30)', price: 6990 } ] },
    { name: 'palta', base: 'Palta', cat: 'Verduras', kcal: 160, options: [
      { label: 'Palta 1kg', price: 6990 }, { label: 'Unidad (2da)', price: 1290 } ] },
    { name: 'batata', base: 'Batata', cat: 'Verduras', kcal: 86, options: [
      { label: 'Batata 1kg', price: 1490 }, { label: 'Bolsa 5kg', price: 6490 } ] },
    { name: 'choclo fresco', base: 'Choclo fresco', cat: 'Verduras', kcal: 90, options: [
      { label: 'Choclo 1u', price: 1290 }, { label: 'Docena', price: 13900 } ] },

    /* ================= FRUTAS ================= */
    { name: 'banana', base: 'Banana', cat: 'Frutas', kcal: 89, options: [
      { label: 'Banana 1kg', price: 1650 }, { label: 'Banana manzana 1kg', price: 1850 } ] },
    { name: 'manzana', base: 'Manzana', cat: 'Frutas', kcal: 52, options: [
      { label: 'Manzana roja 1kg', price: 2290 }, { label: 'Manzana verde 1kg', price: 2150 }, { label: 'Manzana (2da) 1kg', price: 1890 } ] },
    { name: 'naranja', base: 'Naranja', cat: 'Frutas', kcal: 47, options: [
      { label: 'Naranja 1kg', price: 1190 }, { label: 'Naranja (2da) 1kg', price: 990 } ] },
    { name: 'mandarina', base: 'Mandarina', cat: 'Frutas', kcal: 53, options: [
      { label: 'Mandarina 1kg', price: 1290 }, { label: 'Mandarina (2da) 1kg', price: 990 } ] },
    { name: 'pera', base: 'Pera', cat: 'Frutas', kcal: 57, options: [
      { label: 'Pera 1kg', price: 2190 }, { label: 'Pera (2da) 1kg', price: 1690 } ] },
    { name: 'frutilla', base: 'Frutillas', cat: 'Frutas', kcal: 32, options: [
      { label: 'Frutillas 500g', price: 2490 }, { label: 'Frutillas 1kg', price: 4590 } ] },
    { name: 'uvas', base: 'Uvas', cat: 'Frutas', kcal: 69, options: [
      { label: 'Uva 1kg', price: 3990 }, { label: 'Uva (2da) 1kg', price: 2990 } ] },
    { name: 'limon', base: 'Limón', cat: 'Frutas', kcal: 29, options: [
      { label: 'Limón 1kg', price: 1490 }, { label: 'Bolsa 2kg', price: 2690 } ] },
    { name: 'limón', base: 'Limón', cat: 'Frutas', kcal: 29, options: [
      { label: 'Limón 1kg', price: 1490 }, { label: 'Bolsa 2kg', price: 2690 } ] },
    { name: 'melon', base: 'Melón', cat: 'Frutas', kcal: 34, options: [
      { label: 'Melón 1kg', price: 2390 }, { label: 'Melón (oferta)', price: 1890 } ] },
    { name: 'sandia', base: 'Sandía', cat: 'Frutas', kcal: 30, options: [
      { label: 'Sandía 1kg', price: 790 }, { label: 'Sandía (unidad)', price: 4490 } ] },
    { name: 'sandía', base: 'Sandía', cat: 'Frutas', kcal: 30, options: [
      { label: 'Sandía 1kg', price: 790 }, { label: 'Sandía (unidad)', price: 4490 } ] },

    /* ================= BEBIDAS ================= */
    { name: 'agua', base: 'Agua mineral', cat: 'Bebidas', kcal: 0, options: [
      { label: 'Villavicencio 2.25L', price: 2399 }, { label: 'Eco de los Andes 2.25L', price: 2490 }, { label: 'Agua de mesa 2L (marca propia)', price: 1290 } ] },
    { name: 'gaseosa', base: 'Gaseosa', cat: 'Bebidas', kcal: 45, options: [
      { label: 'Coca-Cola 2.25L', price: 3499 }, { label: 'Pepsi 2.25L', price: 3190 }, { label: 'Manaos 2.25L', price: 1690 } ] },
    { name: 'cerveza', base: 'Cerveza', cat: 'Bebidas', kcal: 43, options: [
      { label: 'Quilmes 1L', price: 2699 }, { label: 'Patagonia 473ml', price: 1990 }, { label: 'Andes 473ml', price: 1850 } ] },
    { name: 'jugo', base: 'Jugo', cat: 'Bebidas', kcal: 45, options: [
      { label: 'Cepita 1L', price: 2290 }, { label: 'Baggio 1L', price: 1990 }, { label: 'Marca propia 1L', price: 1490 } ] },
    { name: 'agua saborizada', base: 'Agua saborizada', cat: 'Bebidas', kcal: 30, options: [
      { label: 'Levité 1.25L', price: 1990 }, { label: 'Ser 1.25L', price: 1790 }, { label: 'Marca propia 1.25L', price: 1190 } ] },
    { name: 'gatorade', base: 'Bebida deportiva', cat: 'Bebidas', kcal: 22, options: [
      { label: 'Gatorade 1L', price: 2499 }, { label: 'Powerade 1L', price: 2190 }, { label: 'Marca propia 1L', price: 1490 } ] },
    { name: 'vinos', base: 'Vino', cat: 'Bebidas', kcal: 83, options: [
      { label: 'Vino tinto 750ml', price: 4990 }, { label: 'Vino (2da marca) 750ml', price: 3490 } ] },

    /* ================= LIMPIEZA / BEBIDAS CALIENTES (adicional) ================= */
    { name: 'jabon', base: 'Jabón', cat: 'Limpieza', kcal: 0, options: [
      { label: 'Jabón tocador 3u', price: 1899 }, { label: 'Marca propia 3u', price: 1290 } ] },
    { name: 'detergente', base: 'Detergente', cat: 'Limpieza', kcal: 0, options: [
      { label: 'Magistral 750ml', price: 1499 }, { label: 'Marca propia 750ml', price: 990 } ] },
    { name: 'lavandina', base: 'Lavandina', cat: 'Limpieza', kcal: 0, options: [
      { label: 'Ayudín 1L', price: 999 }, { label: 'Marca propia 1L', price: 690 } ] },
    { name: 'shampoo', base: 'Shampoo', cat: 'Limpieza', kcal: 0, options: [
      { label: 'Pantene 400ml', price: 3499 }, { label: 'Plusbelle 400ml', price: 2290 }, { label: 'Marca propia 400ml', price: 1490 } ] },
    { name: 'papel', base: 'Papel higiénico', cat: 'Limpieza', kcal: 0, options: [
      { label: 'Higgia 4u', price: 2499 }, { label: 'Elite 4u', price: 1990 }, { label: 'Marca propia 4u', price: 1490 } ] },
    { name: 'servilletas', base: 'Servilletas', cat: 'Limpieza', kcal: 0, options: [
      { label: 'Elite 100u', price: 1299 }, { label: 'Marca propia 100u', price: 890 } ] }
  ];

  const TIPS = [
    'Comprá las segundas marcas: suelen costar hasta 30% menos por el mismo producto.',
    'Verduras y frutas por kilo en verdulería suelen ser más baratas que en bandejas de super.',
    'Compará el precio por unidad, no por presentación: la bolsa de 5kg casi siempre conviene.',
    'Los productos de marca propia del supermercado suelen ser 20-40% más baratos.',
    'Compra el jueves y domingo a la tarde: muchas ofertas de carnes y lácteos se descuentan.'
  ];

  function normalize(s) {
    return String(s || '').toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, ' ').trim();
  }

  // Obtiene la categoría de un producto (para sugerir alternativas del mismo rubro)
  function catOf(name) {
    const n = normalize(name);
    if (!n) return null;
    for (const e of DB) {
      if (e.name === n) return e.cat;
      if (n.includes(e.name) || e.name.includes(n)) return e.cat;
    }
    return null;
  }

  // find the closest DB entry for a product name (same product)
  function match(name) {
    const n = normalize(name);
    if (!n) return null;
    for (const e of DB) {
      if (e.name === n) return e;
    }
    for (const e of DB) {
      if (n.includes(e.name) || e.name.includes(n)) return e;
    }
    return null;
  }

  // Given a product name and optional budget, return same-product recommendations
  function findCheaper(name, currentPrice) {
    const e = match(name);
    if (!e) {
      // No hay referencia del mismo producto: sugerimos alternativas de la misma categoría
      const cat = catOf(name);
      if (!cat) return { found: false, base: name, options: [], savingsPct: null, totalAnnual: null, kcal: null, cat: null };
      return {
        found: false, base: name, options: [], savingsPct: null, totalAnnual: null, kcal: null, cat,
        tip: 'No tenemos ese producto exacto, pero buscá alternativas del rubro ' + cat + ' para comparar precios.'
      };
    }
    const current = currentPrice && currentPrice > 0 ? currentPrice : null;
    const options = e.options.map(o => {
      const diff = current ? current - o.price : null;
      const pct = diff && diff > 0 ? Math.round((diff / current) * 100) : 0;
      return { ...o, diff, pct };
    });
    options.sort((a, b) => (b.diff || b.price) - (a.diff || a.price));

    const best = current ? Math.max(...options.map(o => o.diff || 0)) : null;
    const totalAnnual = best ? Math.round(best * 4 * 12) : null;

    return {
      found: true,
      base: e.base,
      cat: e.cat,
      kcal: e.kcal,
      options,
      current,
      best,
      totalAnnual,
      tip: TIPS[Math.floor(Math.random() * TIPS.length)]
    };
  }

  function tipFor(name) {
    const e = match(name);
    if (e) return TIPS[0];
    return TIPS[Math.floor(Math.random() * TIPS.length)];
  }

  return { findCheaper, match, tipFor, catOf };
})();
