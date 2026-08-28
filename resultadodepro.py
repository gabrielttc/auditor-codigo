dedesJavaScript
const express = require('express');
const mysql = require('mysql2/promise');

const app = express();
app.use(express.json());

const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: 'tu_password',
  database: 'auditor_codigo'
};

// ENDPOINT PRINCIPAL: Auditar código
app.post('/api/auditar', async (req, res) => {
  try {
    const { usuarioId, lenguaje, codigo } = req.body;

    // 1. Validaciones básicas de entrada (IF)
    if (!usuarioId || !lenguaje || !codigo) {
      return res.status(400).json({ error: 'Faltan datos obligatorios para el análisis.' });
    }

    const conexion = await mysql.createConnection(dbConfig);

    // 2. Verificar el usuario y sus límites de consumo
    const [usuarios] = await conexion.execute('SELECT * FROM usuarios WHERE id = ?', [usuarioId]);
    
    if (usuarios.length === 0) {
      await conexion.end();
      return res.status(404).json({ error: 'Usuario no encontrado.' });
    }

    const usuario = usuarios[0];

    // Límite para plan gratuito (ej: máximo 3 auditorías)
    if (usuario.tipo_plan === 'gratuito' && usuario.consultas_realizadas >= 3) {
      await conexion.end();
      return res.status(403).json({ 
        error: 'Haz alcanzado el límite del plan gratuito. Pásate a Premium para revisiones ilimitadas.' 
      });
    }

    // 3. Simulación de la lógica de análisis del código
    // (Aquí conectaremos el motor de IA que evalúa el código)
    const resultadoAnalisis = {
      puntuacion: 85,
      errores_detectados: [
        'Falta manejo de excepciones (try/catch) en la consulta SQL.',
        'La variable "password" no debe guardarse en texto plano.'
      ],
      sugerencia_optimizacion: 'Usar consultas preparadas para evitar Inyección SQL.',
      codigo_corregido: `// Versión optimizada\n${codigo}`
    };

    // 4. Guardar la auditoría en la Base de Datos
    const sqlInsert = 'INSERT INTO auditorias (usuario_id, lenguaje, codigo_enviado, puntuacion_calidad, reporte_resultado) VALUES (?, ?, ?, ?, ?)';
    await conexion.execute(sqlInsert, [
      usuarioId, 
      lenguaje, 
      codigo, 
      resultadoAnalisis.puntuacion, 
      JSON.stringify(resultadoAnalisis)
    ]);

    // 5. Incrementar contador de consultas del usuario
    await conexion.execute('UPDATE usuarios SET consultas_realizadas = consultas_realizadas + 1 WHERE id = ?', [usuarioId]);

    await conexion.end();

    // 6. Responder al Frontend
    res.json({
      mensaje: 'Análisis completado con éxito',
      reporte: resultadoAnalisis
    });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => {
  console.log('Servidor del Auditor de Código activo en http://localhost:3000');
});