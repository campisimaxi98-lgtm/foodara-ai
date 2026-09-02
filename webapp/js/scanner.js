/* FOODARA - Capture module: QR / barcode scanning + photo capture + OFF lookup */

const FoodaraCapture = (() => {
  const OFF_API = 'https://world.openfoodfacts.org/api/v2/product/';
  let qrCodeScanner = null;   // html5-qrcode instance
  let stream = null;          // current camera stream

  // ------- QR / barcode decoding -------
  // Loads the html5-qrcode library on demand from CDN.
  function ensureLib() {
    return new Promise((resolve, reject) => {
      if (window.Html5Qrcode) { resolve(window.Html5Qrcode); return; }
      const s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/html5-qrcode@2.3.8/html5-qrcode.min.js';
      s.async = true;
      s.onload = () => resolve(window.Html5Qrcode);
      s.onerror = () => reject(new Error('No se pudo cargar el lector de códigos'));
      document.head.appendChild(s);
    });
  }

  // Start scanning in the given element id
  async function startScan(elementId, onDecode) {
    await stopScan();
    const Html5Qrcode = await ensureLib();
    const config = {
      fps: 10,
      qrbox: { width: 240, height: 180 },
      aspectRatio: 1.0
    };
    qrCodeScanner = new Html5Qrcode(elementId);
    stream = await qrCodeScanner.start(
      { facingMode: 'environment' },
      config,
      (decodedText) => { if (onDecode) onDecode(decodedText); },
      () => {} // scan failure callback (ignore)
    );
    return true;
  }

  async function stopScan() {
    try {
      if (qrCodeScanner && qrCodeScanner.isScanning) {
        await qrCodeScanner.stop();
      }
    } catch (e) { /* ignore */ }
    qrCodeScanner = null;
  }

  // Make sure camera stream is released
  function releaseStream() {
    if (stream && stream.getVideoTracks) {
      try { stream.getVideoTracks().forEach(t => t.stop()); } catch (e) {}
    }
    stream = null;
  }

  // ------- Open Food Facts lookup -------
  // Resolve an EAN/GTIN barcode into product info (name, brand, nutrition).
  async function lookUpBarcode(code) {
    const c = String(code).trim();
    if (!/^\d{8,13}$/.test(c)) {
      return { ok: false, error: 'Código no válido. Asegurate de enfocar el código de barras.' };
    }
    try {
      const res = await fetch(OFF_API + c + '.json');
      if (!res.ok) throw new Error('http ' + res.status);
      const data = await res.json();
      if (data.status !== 1 || !data.product) {
        return { ok: false, error: 'No encontramos datos para ese código (puede ser un producto no registrado).' };
      }
      const p = data.product;
      const names = [p.product_name_es, p.product_name, p.generic_name_es, p.generic_name]
        .filter(Boolean).map(s => String(s).trim());
      const name = names[0] || 'Producto ' + c;
      const nut = (p.nutriments || {});
      const cal = Math.round(nut['energy-kcal_100g'] || nut['energy-kcal'] || 0);
      const prot = Math.round(nut.proteins_100g || nut.proteins || 0);
      const carb = Math.round(nut.carbohydrates_100g || nut.carbohydrates || 0);
      const fat = Math.round(nut.fat_100g || nut.fat || 0);
      return {
        ok: true,
        barcode: c,
        name,
        brand: p.brands ? String(p.brands).split(',')[0].trim() : '',
        image: p.image_front_small_url || p.image_url || '',
        cal: cal || null,
        prot: prot || null,
        carb: carb || null,
        fat: fat || null,
        quantity: p.quantity || ''
      };
    } catch (e) {
      return { ok: false, error: 'Error de conexión al consultar el producto.' };
    }
  }

  // ------- Photo capture -------
  // Opens a file picker restricted to images. Returns a data URL + the filename.
  function pickPhoto() {
    return new Promise((resolve) => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.capture = 'environment'; // hint to use back camera on mobile
      input.onchange = () => {
        const file = input.files && input.files[0];
        if (!file) return resolve(null);
        const reader = new FileReader();
        reader.onload = () => resolve({ dataUrl: reader.result, fileName: file.name });
        reader.readAsDataURL(file);
      };
      input.click();
    });
  }

  // Heuristic: guess a food category/name from the photo's filename (e.g. "IMG_zapallito.jpg")
  function guessFromFilename(fileName) {
    const base = String(fileName || '').replace(/\.[^.]+$/, '').replace(/^IMG_?\d*_?/i, '').replace(/[_-]+/g, ' ').trim();
    if (!base || /^\d+$/.test(base)) return null;
    return base;
  }

  return { startScan, stopScan, releaseStream, lookUpBarcode, pickPhoto, guessFromFilename };
})();
