-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema SIGESI
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema SIGESI
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `SIGESI` ;
USE `SIGESI` ;

-- -----------------------------------------------------
-- Table `SIGESI`.`partidoPBA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`partidoPBA` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`pais`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`pais` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `coordenadaX` DECIMAL(10,7) NOT NULL DEFAULT 0,
  `coordenadaY` DECIMAL(10,7) NOT NULL DEFAULT 0,
  `nacionalidad` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`provincia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`provincia` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(25) NOT NULL,
  `pais` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_provincia_pais1_idx` (`pais` ASC) VISIBLE,
  CONSTRAINT `fk_provincia_pais1`
    FOREIGN KEY (`pais`)
    REFERENCES `SIGESI`.`pais` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`localidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`localidad` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(100) NOT NULL,
  `partido` INT NULL,
  `provincia` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_localidad_partidoPBA1_idx` (`partido` ASC) VISIBLE,
  INDEX `fk_localidad_provincia1_idx` (`provincia` ASC) VISIBLE,
  CONSTRAINT `fk_localidad_partidoPBA1`
    FOREIGN KEY (`partido`)
    REFERENCES `SIGESI`.`partidoPBA` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_localidad_provincia1`
    FOREIGN KEY (`provincia`)
    REFERENCES `SIGESI`.`provincia` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`tipodocumento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`tipodocumento` (
  `id` INT NOT NULL,
  `tipo` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`persona`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`persona` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `apellidos` VARCHAR(60) NOT NULL,
  `nombres` VARCHAR(60) NOT NULL,
  `nacimientofecha` DATE NOT NULL,
  `nacimientopais` INT NOT NULL,
  `nacionalidad` INT NOT NULL,
  `documentotipo` INT NOT NULL,
  `documentonumero` VARCHAR(16) NOT NULL,
  `documentopaisemisor` INT NOT NULL,
  `domiciliopiso` VARCHAR(4) NULL DEFAULT 'null',
  `domiciliodepartamento` VARCHAR(4) NULL DEFAULT 'null',
  `domiciliobarrio` VARCHAR(30) NULL DEFAULT 'null',
  `domiciliolocalidad` INT NOT NULL,
  `domicilioCPA` VARCHAR(8) NOT NULL,
  `domicilioCP4` VARCHAR(4) NOT NULL,
  `domiciliocoordenadaX` DECIMAL(10,7) NOT NULL,
  `domiciliocoordenadaY` DECIMAL(10,7) NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_persona_localidad1_idx` (`domiciliolocalidad` ASC) VISIBLE,
  INDEX `fk_persona_pais1_idx` (`documentopaisemisor` ASC) VISIBLE,
  INDEX `fk_persona_pais2_idx` (`nacimientopais` ASC) VISIBLE,
  INDEX `fk_persona_tipodocumento1_idx` (`documentotipo` ASC) VISIBLE,
  INDEX `fk_persona_pais3_idx` (`nacionalidad` ASC) VISIBLE,
  CONSTRAINT `fk_persona_localidad1`
    FOREIGN KEY (`domiciliolocalidad`)
    REFERENCES `SIGESI`.`localidad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_persona_pais1`
    FOREIGN KEY (`documentopaisemisor`)
    REFERENCES `SIGESI`.`pais` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_persona_pais2`
    FOREIGN KEY (`nacimientopais`)
    REFERENCES `SIGESI`.`pais` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_persona_tipodocumento1`
    FOREIGN KEY (`documentotipo`)
    REFERENCES `SIGESI`.`tipodocumento` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_persona_pais3`
    FOREIGN KEY (`nacionalidad`)
    REFERENCES `SIGESI`.`pais` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`escuela`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`escuela` (
  `CUE` VARCHAR(9) NOT NULL,
  `gestion` VARCHAR(20) NOT NULL,
  `ambito` VARCHAR(20) NOT NULL,
  `tecnica` BOOLEAN NOT NULL,
  `nombre` VARCHAR(150) NOT NULL,
  `domiciliocalle` VARCHAR(150) NOT NULL,
  `domicilioaltura` INT NOT NULL,
  `domiciliolocalidad` INT NOT NULL,
  `domicilioCPA` VARCHAR(4) NOT NULL,
  `domicilioCP4` VARCHAR(8) NOT NULL,
  `domiciliocoordenadaX` FLOAT NOT NULL DEFAULT 0,
  `domiciliocoordenadaY` FLOAT NOT NULL DEFAULT 0,
  PRIMARY KEY (`CUE`),
  INDEX `fk_escuela_localidad1_idx` (`domiciliolocalidad` ASC) VISIBLE,
  CONSTRAINT `fk_escuela_localidad1`
    FOREIGN KEY (`domiciliolocalidad`)
    REFERENCES `SIGESI`.`localidad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`telefonoEscuela`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`telefonoEscuela` (
  `id` INT NOT NULL,
  `telefono` VARCHAR(45) NOT NULL,
  `escuela` VARCHAR(9) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_telefonoEscuela_escuela1_idx` (`escuela` ASC) VISIBLE,
  CONSTRAINT `fk_telefonoEscuela_escuela1`
    FOREIGN KEY (`escuela`)
    REFERENCES `SIGESI`.`escuela` (`CUE`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`mailEscuela`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`mailEscuela` (
  `id` INT NOT NULL,
  `mail` VARCHAR(150) NOT NULL,
  `escuela` VARCHAR(9) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_mailEscuela_escuela1_idx` (`escuela` ASC) VISIBLE,
  CONSTRAINT `fk_mailEscuela_escuela1`
    FOREIGN KEY (`escuela`)
    REFERENCES `SIGESI`.`escuela` (`CUE`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`genero`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`genero` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
-- -----------------------------------------------------
-- Table `SIGESI`.`docente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`docente` (
  `id` INT NOT NULL,
  `cbu` INT NOT NULL,
  `genero` INT NOT NULL,
  `persona` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_docente_persona1_idx` (`persona` ASC) VISIBLE,
  INDEX `fk_docente_genero1_idx` (`genero` ASC) VISIBLE,
  CONSTRAINT `fk_docente_persona1`
    FOREIGN KEY (`persona`)
    REFERENCES `SIGESI`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_docente_genero1`
    FOREIGN KEY (`genero`)
    REFERENCES `SIGESI`.`genero` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`tituloescuela`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`tituloescuela` (
  `id` INT NOT NULL,
  `titulo` VARCHAR(45) NOT NULL,
  `tecnico` BOOLEAN NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`estudiante`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`estudiante` (
  `credencial` INT NOT NULL,
  `legajo` INT NOT NULL DEFAULT 0,
  `cuil` VARCHAR(13) NULL,
  `sexo` CHAR(1) NULL,
  `genero` INT NULL,
  `nombreautopercibido` VARCHAR(60) NULL,
  `escuela` CHAR(9) NULL,
  `escuelaanioegreso` INT NULL,
  `tituloescuela` INT NULL,
  `emergenciatelefono` VARCHAR(20) NULL,
  `emergenciacontacto` VARCHAR(60) NULL,
  `especialidad` INT NULL,
  `turno` CHAR(1) NULL,
  `modalidad` INT NULL,
  `persona` INT NOT NULL,
  PRIMARY KEY (`credencial`),
  INDEX `fk_estudiante_escuela1_idx` (`escuela` ASC) VISIBLE,
  INDEX `fk_estudiante_persona1_idx` (`persona` ASC) VISIBLE,
  INDEX `fk_estudiante_tituloescuela1_idx` (`tituloescuela` ASC) VISIBLE,
  INDEX `fk_estudiante_genero1_idx` (`genero` ASC) VISIBLE,
  CONSTRAINT `fk_estudiante_escuela1`
    FOREIGN KEY (`escuela`)
    REFERENCES `SIGESI`.`escuela` (`CUE`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_estudiante_persona1`
    FOREIGN KEY (`persona`)
    REFERENCES `SIGESI`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_estudiante_tituloescuela1`
    FOREIGN KEY (`tituloescuela`)
    REFERENCES `SIGESI`.`tituloescuela` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_estudiante_genero1`
    FOREIGN KEY (`genero`)
    REFERENCES `SIGESI`.`genero` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`imagenes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`imagenes` (
  `id` INT NOT NULL,
  `tipo` INT NULL,
  `ubicacion` VARCHAR(100) NULL,
  `persona` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_imagenes_persona1_idx` (`persona` ASC) VISIBLE,
  CONSTRAINT `fk_imagenes_persona1`
    FOREIGN KEY (`persona`)
    REFERENCES `SIGESI`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`aula`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`aula` (
  `id` INT NOT NULL,
  `denominacion` VARCHAR(20) NOT NULL,
  `capacidad` INT NOT NULL,
  `aire` BOOLEAN NOT NULL,
  `proyector` BOOLEAN NOT NULL,
  `accesibilidad` BOOLEAN NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`modalidadcursada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`modalidadcursada` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(15) NOT NULL,
  `descripcion` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`comision`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`comision` (
  `id` INT NOT NULL,
  `aula` INT NOT NULL,
  `nombre` VARCHAR(4) NOT NULL,
  `modalidadcursada` INT NOT NULL,
  `ingresoanio` INT NOT NULL,
  INDEX `fk_comisionubicacion_aulas1_idx` (`aula` ASC) VISIBLE,
  INDEX `fk_comision_modalidadcursada1_idx` (`modalidadcursada` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_comisionubicacion_aulas1`
    FOREIGN KEY (`aula`)
    REFERENCES `SIGESI`.`aula` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comision_modalidadcursada1`
    FOREIGN KEY (`modalidadcursada`)
    REFERENCES `SIGESI`.`modalidadcursada` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`matricula`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`matricula` (
  `estudiante` INT NOT NULL,
  `comision` INT NOT NULL,
  PRIMARY KEY (`estudiante`, `comision`),
  INDEX `fk_estudiantecursada_comision1_idx` (`comision` ASC) VISIBLE,
  CONSTRAINT `fk_estudiantecursada_estudiante1`
    FOREIGN KEY (`estudiante`)
    REFERENCES `SIGESI`.`estudiante` (`credencial`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_estudiantecursada_comision1`
    FOREIGN KEY (`comision`)
    REFERENCES `SIGESI`.`comision` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`equipodocente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`equipodocente` (
  `comision` INT NOT NULL,
  `docente` INT NOT NULL,
  `profesor` BOOLEAN NOT NULL,
  PRIMARY KEY (`comision`, `docente`),
  INDEX `fk_equipodocente_comision1_idx` (`comision` ASC) VISIBLE,
  CONSTRAINT `fk_equipodocente_docente1`
    FOREIGN KEY (`docente`)
    REFERENCES `SIGESI`.`docente` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_equipodocente_comision1`
    FOREIGN KEY (`comision`)
    REFERENCES `SIGESI`.`comision` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`unidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`unidad` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `detalle` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`clase`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`clase` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `detalle` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`asistencia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`asistencia` (
  `clase_id` INT NOT NULL,
  `comision_id` INT NOT NULL,
  `estudiante_credencial` INT NOT NULL,
  `fechahora` DATETIME NOT NULL,
  PRIMARY KEY (`clase_id`, `comision_id`, `estudiante_credencial`, `fechahora`),
  INDEX `fk_asistencia_clase1_idx` (`clase_id` ASC) VISIBLE,
  INDEX `fk_asistencia_comision1_idx` (`comision_id` ASC) VISIBLE,
  INDEX `fk_asistencia_estudiante1_idx` (`estudiante_credencial` ASC) VISIBLE,
  CONSTRAINT `fk_asistencia_clase1`
    FOREIGN KEY (`clase_id`)
    REFERENCES `SIGESI`.`clase` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_asistencia_comision1`
    FOREIGN KEY (`comision_id`)
    REFERENCES `SIGESI`.`comision` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_asistencia_estudiante1`
    FOREIGN KEY (`estudiante_credencial`)
    REFERENCES `SIGESI`.`estudiante` (`credencial`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`evaluacionunidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`evaluacionunidad` (
  `id` INT NOT NULL,
  `comision` INT NOT NULL,
  `estudiante` INT NOT NULL,
  `unidad` INT NOT NULL,
  `aprobado` BOOLEAN NULL,
  PRIMARY KEY (`id`, `comision`, `estudiante`, `unidad`),
  INDEX `fk_evaluacion_comision1_idx` (`comision` ASC) VISIBLE,
  INDEX `fk_evaluacion_estudiante1_idx` (`estudiante` ASC) VISIBLE,
  INDEX `fk_evaluacion_unidad1_idx` (`unidad` ASC) VISIBLE,
  CONSTRAINT `fk_evaluacion_comision1`
    FOREIGN KEY (`comision`)
    REFERENCES `SIGESI`.`comision` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evaluacion_estudiante1`
    FOREIGN KEY (`estudiante`)
    REFERENCES `SIGESI`.`estudiante` (`credencial`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evaluacion_unidad1`
    FOREIGN KEY (`unidad`)
    REFERENCES `SIGESI`.`unidad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`parcial`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`parcial` (
  `id` INT NOT NULL,
  `estudiante` INT NOT NULL,
  `comision` INT NOT NULL,
  `unidad` INT NOT NULL,
  `nota` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_parcial_comision1_idx` (`comision` ASC) VISIBLE,
  INDEX `fk_parcial_estudiante1_idx` (`estudiante` ASC) VISIBLE,
  INDEX `fk_parcial_unidad1_idx` (`unidad` ASC) VISIBLE,
  CONSTRAINT `fk_parcial_comision1`
    FOREIGN KEY (`comision`)
    REFERENCES `SIGESI`.`comision` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_parcial_estudiante1`
    FOREIGN KEY (`estudiante`)
    REFERENCES `SIGESI`.`estudiante` (`credencial`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_parcial_unidad1`
    FOREIGN KEY (`unidad`)
    REFERENCES `SIGESI`.`unidad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `SIGESI`.`evaluaciondiaria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `SIGESI`.`evaluaciondiaria` (
  `parcial` INT NOT NULL,
  `orden` INT NOT NULL,
  `estudiante` INT NOT NULL,
  `aprobado` BOOLEAN NOT NULL,
  PRIMARY KEY (`parcial`, `orden`),
  INDEX `fk_evaluaciondiaria_parcial1_idx` (`parcial` ASC) VISIBLE,
  INDEX `fk_evaluaciondiaria_estudiante1_idx` (`estudiante` ASC) VISIBLE,
  CONSTRAINT `fk_evaluaciondiaria_parcial1`
    FOREIGN KEY (`parcial`)
    REFERENCES `SIGESI`.`parcial` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evaluaciondiaria_estudiante1`
    FOREIGN KEY (`estudiante`)
    REFERENCES `SIGESI`.`estudiante` (`credencial`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
