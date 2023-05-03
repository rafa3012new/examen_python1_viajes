-- create database viajes_dojo;

use viajes_dojo;

-- se crea la tabla usuarios
CREATE TABLE IF NOT EXISTS  `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- se crea la tabla viajes
CREATE TABLE IF NOT EXISTS `viajes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destino` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `planificador` int NOT NULL,
  `fecha_inicio` datetime NOT NULL,
  `fecha_fin` datetime NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT FK_USUARIO FOREIGN KEY (planificador) REFERENCES usuarios(id) on update cascade on delete cascade
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- se crea la tabla viajes
CREATE TABLE IF NOT EXISTS `participantes` (
  `id_viaje` int NOT NULL,
  `id_participante` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_viaje`, id_participante),
  CONSTRAINT FK_VIAJE_PARTICIPANTE FOREIGN KEY (id_viaje) REFERENCES viajes(id) on update cascade on delete cascade,
  CONSTRAINT FK_USUARIO_PARTICIPANTE FOREIGN KEY (id_participante) REFERENCES usuarios(id) on update cascade on delete cascade
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;