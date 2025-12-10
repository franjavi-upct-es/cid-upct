analizar_modelo <- function(serie_temporal) {
  # Obtener frecuencia de la serie
  freq <- frequency(serie_temporal)

  # Calcular medias y desviaciones típicas
  if (freq == 1) {
    # Para series sin estacionalidad, usar ventanas móviles
    window_size <- min(12, floor(length(serie_temporal) / 4))
    n_windows <- floor(length(serie_temporal) / window_size)
    medias_anuales <- numeric(n_windows)
    desviaciones_anuales <- numeric(n_windows)

    for (i in 1:n_windows) {
      start_idx <- (i - 1) * window_size + 1
      end_idx <- min(i * window_size, length(serie_temporal))
      ventana <- serie_temporal[start_idx:end_idx]
      medias_anuales[i] <- mean(ventana)
      desviaciones_anuales[i] <- sd(ventana)
    }
  } else {
    # Para series estacionales, usar aggregate
    medias_anuales <- as.vector(aggregate(serie_temporal, FUN = mean))
    desviaciones_anuales <- as.vector(aggregate(serie_temporal, FUN = sd))
  }

  # Realizar regresión lineal
  modelo_regresion <- lm(desviaciones_anuales ~ medias_anuales)
  pendiente <- coef(modelo_regresion)[2]
  r_cuadrado <- summary(modelo_regresion)$r.squared

  # Determinar tipo de modelo
  if (r_cuadrado > 0.5 && pendiente > 0.1) {
    tipo_modelo <- "MULTIPLICATIVO"
    cat("TIPO DE MODELO: MULTIPLICATIVO\n")
    cat("(La desviación típica aumenta con la media)\n\n")
  } else {
    tipo_modelo <- "ADITIVO"
    cat("TIPO DE MODELO: ADITIVO\n")
    cat("(La desviación típica es relativamente constante)\n\n")
  }

  # Analizar componentes
  cat("COMPONENTES DETECTADAS:\n")

  # Componente estacional
  if (freq > 1) {
    cat("✓ Componente ESTACIONAL: SÍ (frecuencia =", freq, ")\n")
  } else {
    cat("✗ Componente ESTACIONAL: NO\n")
  }

  # Componente tendencia-ciclo
  if (freq > 1) {
    # Para series estacionales, usar decompose
    descomposicion <- decompose(serie_temporal,
      type = ifelse(tipo_modelo == "MULTIPLICATIVO", "multiplicative", "additive")
    )
    tendencia <- descomposicion$trend
  } else {
    # Para series no estacionales, usar suavizado loess
    tiempo <- 1:length(serie_temporal)
    suavizado <- loess(as.vector(serie_temporal) ~ tiempo, span = 0.3)
    tendencia <- suavizado$fitted
    descomposicion <- NULL
  }

  rango_tendencia <- diff(range(tendencia, na.rm = TRUE))
  rango_serie <- diff(range(serie_temporal, na.rm = TRUE))

  if (rango_tendencia / rango_serie > 0.3) {
    cat("✓ Componente TENDENCIA-CICLO: SÍ\n")
  } else {
    cat("✗ Componente TENDENCIA-CICLO: NO significativa\n")
  }

  # Componente irregular
  if (freq > 1) {
    irregular <- descomposicion$random
    cv_irregular <- sd(irregular, na.rm = TRUE) / mean(serie_temporal, na.rm = TRUE)
  } else {
    # Para series no estacionales, calcular residuos del suavizado
    irregular <- serie_temporal - tendencia
    cv_irregular <- sd(irregular, na.rm = TRUE) / mean(serie_temporal, na.rm = TRUE)
  }

  if (cv_irregular > 0.05) {
    cat("✓ Componente IRREGULAR: SÍ (CV =", round(cv_irregular, 4), ")\n")
  } else {
    cat("✗ Componente IRREGULAR: Muy débil\n")
  }

  # Retornar información
  invisible(list(
    tipo = tipo_modelo,
    pendiente = pendiente,
    r_cuadrado = r_cuadrado,
    descomposicion = descomposicion
  ))
}
