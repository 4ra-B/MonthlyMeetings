# MonthlyMeetings

Financial Metrics – Admin Panel

Panel administrativo desarrollado con Streamlit para la gestión y visualización de métricas financieras, conectado a Supabase como base de datos.

Permite:
- Insertar y actualizar datos financieros mensuales
- Generar gráficos financieros clave
- Descargar los gráficos en formato PNG
- Analizar ingresos, costes y forecast por periodo
- Analizar ingresos por país

Stack Tecnológico
- Python 3.10+
- Streamlit – interfaz web
- Supabase – base de datos (PostgreSQL)
- Pandas – procesamiento de datos
- Matplotlib – visualización de gráficos

Instalación Local
1. Clona el repositorio:
git clone https://github.com/tu-usuario/financial-metrics-panel.git
cd financial-metrics-panel

2. Crea un entorno virtual (opcional pero recomendado):
python -m venv venv
source venv/bin/activate  # Mac / Linux
venv\Scripts\activate     # Windows

3. Instala dependencias:
pip install -r requirements.txt

4. Ejecuta la app:
streamlit run app.py

Funcionalidades del Dashboard
- Inserción / actualización de datos
  *Formulario mensual
  *Upsert automático por month_year
- Gráfico: Último mes
  *Ingresos reales vs forecast
  *Costes + EBITDAC
  *Comparación visual clara
- Gráfico: Año natural
  *Acumulado desde enero
  *Real vs forecast
- Gráfico: Ingresos por país
  *Últimos 12 meses
  *España (SaaS), Chile y Brasil
  Visualización temporal
- Exportación
  *Descarga de cada gráfico en PNG

Seguridad
- No se almacenan credenciales en el código
- Acceso a la base de datos vía variables de entorno
- Recomendado usar Row Level Security (RLS) en Supabase

Autor
Proyecto desarrollado como panel interno de control financiero y base para futuros módulos de Business Intelligence - Laura Benkel Brander.
