
# 🧾 Telegram Gastos Bot

Un bot de Telegram en Python para registrar tus gastos de supermercados o negocios escribiendo el nombre y el monto, y visualizar un resumen en un gráfico.

## 📸 ¿Qué hace este bot?

- Registra los gastos ingresados por el usuario con el formato: `nombre_del_comercio monto` (por ejemplo: `coto 15879.50`)
- Guarda los datos por usuario en una base de datos SQLite
- Permite ver un gráfico resumen por comercio que muestra:
  - Cuántas veces se gastó en cada lugar
  - Cuánto dinero se gastó en total por comercio

## 🛠 Tecnologías usadas

- Python 3.11+ (recomendado: 3.11 o 3.12)
- `python-telegram-bot` (20.7)
- `matplotlib`
- `httpx`
- `dotenv`
- `sqlite3` (incluido en Python)

## 📦 Instalación local

1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/telegram-gastos-bot.git
cd telegram-gastos-bot
```

2. Crear el entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

4. Crear un archivo `.env` con tu token

Crear un archivo llamado `.env` en la raíz del proyecto con este contenido:

```env
TELEGRAM_TOKEN=TU_TOKEN_DEL_BOT
```

5. Ejecutar el bot

```bash
python main.py
```

## 👤 ¿Cómo usarlo?

- Enviar un mensaje al bot con el nombre del comercio y el monto:
  Ejemplo: `carrefour 4567.89`

- Usar el comando `/resumen` para ver un gráfico de tus gastos por comercio

## 📊 Comandos disponibles

- `/start` — Mensaje de bienvenida y explicación del bot  
- `/resumen` — Genera un gráfico con el total gastado y la cantidad de visitas por comercio  

## 🗃 Estructura del proyecto

```
.
├── main.py              # Código principal del bot
├── db.py                # Módulo para crear y guardar en la base de datos SQLite
├── .env                 # Archivo oculto con el token del bot
├── requirements.txt     # Lista de dependencias
└── README.md            # Este archivo
```

## 📄 Licencia

Este proyecto está licenciado bajo MIT License.

## 🙌 Agradecimientos

Creado por Agustín Nadal ([telegram.me/TU_USUARIO](https://t.me/TU_USUARIO))
