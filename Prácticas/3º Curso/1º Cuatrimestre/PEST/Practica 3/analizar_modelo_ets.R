analizar_modelo_ETS <- function(serie_temporal) {
  cat("=== ANÁLISIS PARA SELECCIÓN DE MODELO ETS ===\n\n")

  # 1. ANÁLISIS DEL TIPO DE ERROR/VARIABILIDAD
  cat("1) ANÁLISIS DEL COMPONENTE DE ERROR:\n")

  # Para series con frequency = 1, calculamos ventanas móviles
  freq <- frequency(serie_temporal)
  if (freq == 1) {
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
    medias_anuales <- as.vector(aggregate(serie_temporal, FUN = mean))
    desviaciones_anuales <- as.vector(aggregate(serie_temporal, FUN = sd))
  }

  modelo_regresion <- lm(desviaciones_anuales ~ medias_anuales)
  pendiente <- coef(modelo_regresion)[2]
  r_cuadrado <- summary(modelo_regresion)$r.squared

  if (r_cuadrado > 0.5 && pendiente > 0.1) {
    tipo_error <- "M"
    cat("   → Error MULTIPLICATIVO (M)\n")
    cat("   Razón: La desviación típica aumenta con la media\n")
    cat("   (R² =", round(r_cuadrado, 3), ", pendiente =", round(pendiente, 3), ")\n\n")
  } else {
    tipo_error <- "A"
    cat("   → Error ADITIVO (A)\n")
    cat("   Razón: La desviación típica es relativamente constante\n")
    cat("   (R² =", round(r_cuadrado, 3), ", pendiente =", round(pendiente, 3), ")\n\n")
  }

  # 2. ANÁLISIS DE LA TENDENCIA
  cat("2) ANÁLISIS DEL COMPONENTE DE TENDENCIA:\n")

  # Para frequency = 1, usamos suavizado loess en lugar de decompose
  if (freq == 1) {
    tiempo <- 1:length(serie_temporal)
    suavizado <- loess(as.vector(serie_temporal) ~ tiempo, span = 0.3)
    tendencia <- suavizado$fitted
  } else {
    descomposicion <- decompose(serie_temporal,
      type = ifelse(tipo_error == "M", "multiplicative", "additive")
    )
    tendencia <- descomposicion$trend
  }

  rango_tendencia <- diff(range(tendencia, na.rm = TRUE))
  rango_serie <- diff(range(serie_temporal, na.rm = TRUE))
  ratio_tendencia <- rango_tendencia / rango_serie

  # Calcular pendiente de la tendencia
  tiempo <- 1:length(tendencia)
  modelo_tend <- lm(tendencia ~ tiempo, na.action = na.omit)
  pendiente_tend <- abs(coef(modelo_tend)[2])

  if (ratio_tendencia > 0.3 && pendiente_tend > 0.01) {
    if (tipo_error == "M") {
      tipo_tendencia <- "M"
      cat("   → Tendencia MULTIPLICATIVA (M)\n")
      cat("   Razón: Tendencia significativa con crecimiento proporcional\n")
    } else {
      tipo_tendencia <- "A"
      cat("   → Tendencia ADITIVA (A)\n")
      cat("   Razón: Tendencia significativa con crecimiento constante\n")
    }
    cat("   (Ratio tendencia/serie =", round(ratio_tendencia, 3), ")\n\n")
  } else {
    tipo_tendencia <- "N"
    cat("   → Tendencia AUSENTE (N)\n")
    cat("   Razón: No se detecta tendencia significativa\n")
    cat("   (Ratio tendencia/serie =", round(ratio_tendencia, 3), ")\n\n")
  }

  # 3. ANÁLISIS DE LA ESTACIONALIDAD
  cat("3) ANÁLISIS DEL COMPONENTE ESTACIONAL:\n")

  if (freq > 1) {
    descomposicion <- decompose(serie_temporal,
      type = ifelse(tipo_error == "M", "multiplicative", "additive")
    )
    estacional <- descomposicion$seasonal
    rango_estacional <- diff(range(estacional, na.rm = TRUE))
    ratio_estacional <- rango_estacional / rango_serie

    # Calcular coeficiente de variación de la amplitud estacional
    if (tipo_error == "M") {
      amplitudes_estacionales <- tapply(estacional, cycle(serie_temporal), function(x) mean(x, na.rm = TRUE))
    } else {
      amplitudes_estacionales <- tapply(abs(estacional), cycle(serie_temporal), function(x) mean(x, na.rm = TRUE))
    }
    cv_estacional <- sd(amplitudes_estacionales, na.rm = TRUE) / mean(abs(amplitudes_estacionales), na.rm = TRUE)

    if (ratio_estacional > 0.1) {
      if (tipo_error == "M" && cv_estacional > 0.2) {
        tipo_estacional <- "M"
        cat("   → Estacionalidad MULTIPLICATIVA (M)\n")
        cat("   Razón: Amplitud estacional crece proporcionalmente con el nivel\n")
      } else {
        tipo_estacional <- "A"
        cat("   → Estacionalidad ADITIVA (A)\n")
        cat("   Razón: Amplitud estacional constante a lo largo del tiempo\n")
      }
      cat("   (Frecuencia =", freq, ", Ratio estacional/serie =", round(ratio_estacional, 3), ")\n\n")
    } else {
      tipo_estacional <- "N"
      cat("   → Estacionalidad AUSENTE (N)\n")
      cat("   Razón: Patrón estacional muy débil o inexistente\n\n")
    }
  } else {
    tipo_estacional <- "N"
    cat("   → Estacionalidad AUSENTE (N)\n")
    cat("   Razón: Frecuencia = 1, no hay periodicidad\n\n")
  }

  # 4. MODELO ETS RECOMENDADO
  modelo_ets <- paste0("ETS(", tipo_error, ",", tipo_tendencia, ",", tipo_estacional, ")")

  cat("========================================\n")
  cat("MODELO ETS RECOMENDADO:", modelo_ets, "\n")
  cat("========================================\n\n")

  cat("INTERPRETACIÓN:\n")
  cat("- Error:", ifelse(tipo_error == "A", "Aditivo", "Multiplicativo"), "\n")
  cat(
    "- Tendencia:",
    switch(tipo_tendencia,
      "A" = "Aditiva (crecimiento constante)",
      "M" = "Multiplicativa (crecimiento proporcional)",
      "N" = "Ninguna (sin tendencia)"
    ), "\n"
  )
  cat(
    "- Estacionalidad:",
    switch(tipo_estacional,
      "A" = "Aditiva (amplitud constante)",
      "M" = "Multiplicativa (amplitud variable)",
      "N" = "Ninguna (sin estacionalidad)"
    ), "\n\n"
  )

  # Equivalencia con Holt-Winters
  if (tipo_tendencia != "N" && tipo_estacional != "N") {
    metodo_hw <- ifelse(tipo_estacional == "A",
      "Holt-Winters aditivo",
      "Holt-Winters multiplicativo"
    )
    cat("EQUIVALENCIA: Este modelo corresponde al método", metodo_hw, "\n\n")
  } else if (tipo_tendencia != "N" && tipo_estacional == "N") {
    cat("EQUIVALENCIA: Este modelo corresponde al método de Holt\n\n")
  } else if (tipo_tendencia == "N" && tipo_estacional == "N") {
    cat("EQUIVALENCIA: Este modelo corresponde al alisado exponencial simple\n\n")
  }

  # Retornar información
  descomp_result <- if (freq > 1) descomposicion else NULL

  invisible(list(
    modelo = modelo_ets,
    error = tipo_error,
    tendencia = tipo_tendencia,
    estacionalidad = tipo_estacional,
    r_cuadrado = r_cuadrado,
    pendiente = pendiente,
    descomposicion = descomp_result
  ))
}
