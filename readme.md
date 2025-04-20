## 1. Crear un entorno virtual

```bash
python3 -m venv .venv
```

> Esto crea un entorno virtual en la carpeta `.venv`.

### Activar el entorno virtual

- **Linux/macOS:**

  ```bash
  source .venv/bin/activate
  ```

- **Windows (CMD):**

  ```cmd
  .venv\Scripts\activate
  ```

- **Windows (PowerShell):**

  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

- Una vez activado, instalá las dependencias del proyecto con:
  ```bash
  pip install -r requirements.txt
  ```

---

## 2. Realizar migraciones iniciales

Desde la raíz del proyecto Django:

```bash
python manage.py makemigrations
python manage.py migrate
```

> Esto crea las tablas iniciales en la base de datos.

---

## 3. Crear un superusuario

```bash
python manage.py createsuperuser
```

Ingresá los datos que se solicitan (usuario, email, contraseña).

---

## ¡Listo!

Tu entorno está configurado y tu base de datos inicial ya está en marcha. Ahora podés ejecutar el servidor con:

```bash
python manage.py runserver
```

---
