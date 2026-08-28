const express = require('express');
const mysql = require('mysql2/promise');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname)));

const JWT_SECRET = process.env.JWT_SECRET || 'secreto_super_seguro_auditor';

// Conexión a la base de datos MySQL (Aiven)
const dbConfig = {
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  ssl: { rejectUnauthorized: false }
};

// Inicializar tablas en la Base de Datos
async function initDB() {
  try {
    const connection = await mysql.createConnection(dbConfig);
    
    // Tabla de Usuarios (cada usuario arranca con 5 créditos de regalo)
    await connection.query(`
      CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        creditos INT DEFAULT 5,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Tabla de Auditorías vinculada al usuario
    await connection.query(`
      CREATE TABLE IF NOT EXISTS auditorias (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT,
        codigo TEXT NOT NULL,
        resultado TEXT NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
      )
    `);

    console.log('✅ Tablas en MySQL inicializadas correctamente');
    await connection.end();
  } catch (err) {
    console.error('❌ Error al inicializar tablas en MySQL:', err.message);
  }
}

initDB();

// RUTAS DE AUTENTICACIÓN

// 1. Registro de usuario
app.post('/api/registro', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ error: 'Email y contraseña requeridos' });

  try {
    const connection = await mysql.createConnection(dbConfig);
    const hashedPassword = await bcrypt.hash(password, 10);

    const [result] = await connection.query(
      'INSERT INTO usuarios (email, password, creditos) VALUES (?, ?, 5)',
      [email, hashedPassword]
    );

    await connection.end();
    res.json({ mensaje: 'Usuario registrado con éxito', usuarioId: result.insertId });
  } catch (err) {
    if (err.code === 'ER_DUP_ENTRY') {
      return res.status(400).json({ error: 'El email ya está registrado' });
    }
    res.status(500).json({ error: 'Error al registrar el usuario' });
  }
});

// 2. Login de usuario
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ error: 'Email y contraseña requeridos' });

  try {
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.query('SELECT * FROM usuarios WHERE email = ?', [email]);
    await connection.end();

    if (rows.length === 0) return res.status(400).json({ error: 'Usuario no encontrado' });

    const usuario = rows[0];
    const passwordValido = await bcrypt.compare(password, usuario.password);
    if (!passwordValido) return res.status(400).json({ error: 'Contraseña incorrecta' });

    // Generar Token JWT válido por 24 horas
    const token = jwt.sign({ id: usuario.id, email: usuario.email }, JWT_SECRET, { expiresIn: '24h' });

    res.json({
      mensaje: 'Inicio de sesión exitoso',
      token,
      usuario: { id: usuario.id, email: usuario.email, creditos: usuario.creditos }
    });
  } catch (err) {
    res.status(500).json({ error: 'Error en el inicio de sesión' });
  }
});

// 3. Endpoint de Auditoría (Integrado con Gemini API)
app.post('/api/auditar', async (req, res) => {
  const { codigo } = req.body;
  const apiKey = process.env.GEMINI_API_KEY;

  if (!codigo) return res.status(400).json({ error: 'No se envió código' });
  if (!apiKey) return res.status(500).json({ error: 'Falta GEMINI_API_KEY en variables de entorno' });

  try {
    const prompt = `Actúa como un Auditor Senior de Código y Ciberseguridad. Analiza el siguiente código, detecta vulnerabilidades, malas prácticas y ofrece el código corregido de forma clara:\n\n${codigo}`;

    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=${apiKey}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
    });

    const data = await response.json();
    const analisis = data.candidates?.[0]?.content?.parts?.[0]?.text || 'No se pudo generar el análisis.';

    // Guardar en MySQL
    const connection = await mysql.createConnection(dbConfig);
    const [result] = await connection.query(
      'INSERT INTO auditorias (codigo, resultado) VALUES (?, ?)',
      [codigo, analisis]
    );
    await connection.end();

    res.json({ analisis, id_registro: result.insertId });
  } catch (err) {
    res.status(500).json({ error: 'Error procesando auditoría', detalle: err.message });
  }
});

// 4. Historial de Auditorías
app.get('/api/auditorias', async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.query('SELECT * FROM auditorias ORDER BY id DESC LIMIT 10');
    await connection.end();
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: 'Error al consultar historial' });
  }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`🚀 Servidor corriendo en el puerto ${PORT}`);
});