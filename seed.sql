-- Datos de prueba (cargar después de schema.sql)
INSERT INTO usuarios (nombre, email) VALUES
 ('Michael Mejia', 'michael.mejia@mesa.local'),
 ('Soporte Nivel 1', 'nivel1@mesa.local'),
 ('Soporte Nivel 2', 'nivel2@mesa.local');

INSERT INTO categorias (nombre) VALUES
 ('Hardware'), ('Software'), ('Red / Conectividad'), ('Cuentas y accesos'), ('Otro');

INSERT INTO tickets (codigo, solicitante, titulo, descripcion, categoria_id, prioridad, estado, responsable_id) VALUES
 ('TCK-0001','Ana Rojas','Impresora no imprime','La impresora del piso 2 no responde.',1,'Media','Nuevo',NULL),
 ('TCK-0002','Luis Soto','Sin acceso a correo','No puedo ingresar a mi correo corporativo.',4,'Alta','En proceso',2),
 ('TCK-0003','Carla Pino','Instalar Office','Necesito instalar Office en mi equipo nuevo.',2,'Baja','Resuelto',1),
 ('TCK-0004','Pedro Díaz','WiFi caído en sala 3','Sin red inalámbrica desde la mañana.',3,'Crítica','En proceso',3),
 ('TCK-0005','Marta León','Cambio de teclado','Teclado con teclas defectuosas.',1,'Baja','Cerrado',2);
