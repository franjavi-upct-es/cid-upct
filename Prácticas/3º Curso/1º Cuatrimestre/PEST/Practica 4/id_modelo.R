analizar_arima <- function(serie_temporal, max_p = 5, max_q = 5, max_d = 2) {
  library(forecast)
  library(tseries)

  cat("════════════════════════════════════════════════════════════════\n")
  cat("   ANÁLISIS TEÓRICO PARA IDENTIFICACIÓN DE MODELO ARIMA\n")
  cat("════════════════════════════════════════════════════════════════\n\n")

  # ============================================================
  # 1. ANÁLISIS DE ESTACIONARIEDAD
  # ============================================================
  cat("═══ 1. ANÁLISIS DE ESTACIONARIEDAD ═══\n\n")

  serie_original <- serie_temporal
  d <- 0

  # Test ADF (Augmented Dickey-Fuller)
  adf_test <- adf.test(serie_temporal, alternative = "stationary")
  cat("📊 Test ADF (Augmented Dickey-Fuller):\n")
  cat("   H0: La serie NO es estacionaria (tiene raíz unitaria)\n")
  cat("   H1: La serie SÍ es estacionaria\n")
  cat("   p-valor =", round(adf_test$p.value, 4), "\n")

  if (adf_test$p.value > 0.05) {
    cat("   ⚠ p-valor > 0.05 → NO rechazamos H0\n")
    cat("   CONCLUSIÓN: La serie NO es estacionaria\n")
    cat("   ACCIÓN: Se requiere diferenciación (d > 0)\n\n")

    # Determinar orden de diferenciación
    serie_diff <- serie_temporal
    d <- 0

    for (i in 1:max_d) {
      serie_diff <- diff(serie_diff)
      d <- d + 1
      adf_diff <- adf.test(serie_diff, alternative = "stationary")

      cat("   Diferenciación orden", d, ":\n")
      cat("   p-valor ADF =", round(adf_diff$p.value, 4), "\n")

      if (adf_diff$p.value <= 0.05) {
        cat("   ✓ Serie estacionaria después de", d, "diferenciación(es)\n\n")
        serie_temporal <- serie_diff
        break
      } else {
        cat("   ✗ Aún no es estacionaria\n\n")
      }
    }
  } else {
    cat("   ✓ p-valor ≤ 0.05 → Rechazamos H0\n")
    cat("   CONCLUSIÓN: La serie SÍ es estacionaria\n")
    cat("   ACCIÓN: No se requiere diferenciación (d = 0)\n\n")
  }

  cat("► ORDEN DE DIFERENCIACIÓN: d =", d, "\n\n")

  # ============================================================
  # 2. ANÁLISIS DE CORRELOGRAMAS
  # ============================================================
  cat("═══ 2. ANÁLISIS DE CORRELOGRAMAS (ACF y PACF) ═══\n\n")

  # Calcular ACF y PACF
  acf_values <- acf(serie_temporal, plot = FALSE, lag.max = 40)
  pacf_values <- pacf(serie_temporal, plot = FALSE, lag.max = 40)

  # Límites de confianza (95%)
  limite_conf <- 1.96 / sqrt(length(serie_temporal))

  # Analizar ACF
  cat("📈 CORRELOGRAMA SIMPLE (ACF):\n")
  acf_sig <- which(abs(acf_values$acf[-1]) > limite_conf)

  if (length(acf_sig) == 0) {
    cat("   ✓ Todos los rezagos dentro de límites de confianza\n")
    cat("   → Posible ruido blanco o serie ya modelada\n\n")
    q_sugerido <- 0
  } else {
    cat("   Rezagos significativos:", acf_sig[1:min(10, length(acf_sig))], "\n")

    # Detectar patrón de decaimiento
    primeros_5_acf <- abs(acf_values$acf[2:6])

    # Decaimiento exponencial (AR)
    if (all(diff(primeros_5_acf) < 0) && primeros_5_acf[1] > limite_conf * 2) {
      cat("   📉 PATRÓN: Decaimiento exponencial gradual\n")
      cat("   → Característico de proceso AR(p)\n")
      cat("   → El orden p se determina con PACF\n\n")
      patron_acf <- "decaimiento_exponencial"
    }
    # Corte abrupto (MA)
    else if (length(acf_sig) <= 3 && max(acf_sig) <= 5) {
      cat("   ✂ PATRÓN: Corte abrupto después del rezago", max(acf_sig), "\n")
      cat("   → Característico de proceso MA(q)\n")
      cat("   → Orden sugerido: q =", max(acf_sig), "\n\n")
      q_sugerido <- max(acf_sig)
      patron_acf <- "corte_abrupto"
    }
    # Decaimiento sinusoidal (AR con raíces complejas)
    else if (any(acf_values$acf[2:10] < -limite_conf)) {
      cat("   🌊 PATRÓN: Decaimiento sinusoidal (oscilante)\n")
      cat("   → Característico de proceso AR con raíces complejas\n")
      cat("   → El orden p se determina con PACF\n\n")
      patron_acf <- "decaimiento_sinusoidal"
    }
    # Patrón mixto
    else {
      cat("   🔀 PATRÓN: Decaimiento lento o mixto\n")
      cat("   → Posible proceso ARMA(p,q)\n")
      cat("   → Se requiere análisis combinado de ACF y PACF\n\n")
      patron_acf <- "mixto"
      q_sugerido <- length(which(abs(acf_values$acf[2:6]) > limite_conf))
    }
  }

  # Analizar PACF
  cat("📉 CORRELOGRAMA PARCIAL (PACF):\n")
  pacf_sig <- which(abs(pacf_values$acf) > limite_conf)

  if (length(pacf_sig) == 0) {
    cat("   ✓ Todos los rezagos dentro de límites de confianza\n")
    cat("   → No se detecta componente AR\n\n")
    p_sugerido <- 0
  } else {
    cat("   Rezagos significativos:", pacf_sig[1:min(10, length(pacf_sig))], "\n")

    # Corte abrupto en PACF (AR)
    if (length(pacf_sig) <= 3 && max(pacf_sig) <= 5) {
      cat("   ✂ PATRÓN: Corte abrupto después del rezago", max(pacf_sig), "\n")
      cat("   → Característico de proceso AR(p)\n")
      cat("   → Orden sugerido: p =", max(pacf_sig), "\n\n")
      p_sugerido <- max(pacf_sig)
      patron_pacf <- "corte_abrupto"
    }
    # Decaimiento gradual (MA)
    else if (length(pacf_sig) > 5) {
      primeros_5_pacf <- abs(pacf_values$acf[1:5])
      if (all(diff(primeros_5_pacf) < 0)) {
        cat("   📉 PATRÓN: Decaimiento exponencial gradual\n")
        cat("   → Característico de proceso MA(q)\n")
        cat("   → El orden q se determina con ACF\n\n")
        p_sugerido <- 0
        patron_pacf <- "decaimiento_exponencial"
      } else {
        cat("   🔀 PATRÓN: Decaimiento irregular\n")
        cat("   → Posible proceso ARMA(p,q)\n\n")
        p_sugerido <- length(which(abs(pacf_values$acf[1:5]) > limite_conf))
        patron_pacf <- "mixto"
      }
    } else {
      p_sugerido <- max(pacf_sig)
      patron_pacf <- "mixto"
    }
  }

  # ============================================================
  # 3. IDENTIFICACIÓN DEL MODELO
  # ============================================================
  cat("═══ 3. IDENTIFICACIÓN DEL MODELO ARIMA ═══\n\n")

  cat("📋 REGLAS DE IDENTIFICACIÓN:\n")
  cat("┌─────────────────┬──────────────────┬──────────────────┬─────────────┐\n")
  cat("│ Modelo          │ ACF              │ PACF             │ Conclusión  │\n")
  cat("├─────────────────┼──────────────────┼──────────────────┼─────────────┤\n")
  cat("│ AR(p)           │ Decae gradual    │ Corte en p       │ Usar PACF   │\n")
  cat("│ MA(q)           │ Corte en q       │ Decae gradual    │ Usar ACF    │\n")
  cat("│ ARMA(p,q)       │ Decae gradual    │ Decae gradual    │ Ambos       │\n")
  cat("└─────────────────┴──────────────────┴──────────────────┴─────────────┘\n\n")

  # Determinar modelo basado en patrones
  if (!exists("patron_acf")) patron_acf <- "indefinido"
  if (!exists("patron_pacf")) patron_pacf <- "indefinido"
  if (!exists("p_sugerido")) p_sugerido <- 0
  if (!exists("q_sugerido")) q_sugerido <- 0

  cat("🔍 DIAGNÓSTICO:\n")

  if (patron_pacf == "corte_abrupto" &&
    (patron_acf == "decaimiento_exponencial" || patron_acf == "decaimiento_sinusoidal")) {
    cat("   • ACF: Decaimiento gradual\n")
    cat("   • PACF: Corte abrupto en p =", p_sugerido, "\n")
    cat("   ► MODELO IDENTIFICADO: AR(", p_sugerido, ")\n\n")
    modelo_teorico <- paste0("AR(", p_sugerido, ")")
    p_final <- p_sugerido
    q_final <- 0
  } else if (patron_acf == "corte_abrupto" &&
    (patron_pacf == "decaimiento_exponencial" || patron_pacf == "indefinido")) {
    cat("   • ACF: Corte abrupto en q =", q_sugerido, "\n")
    cat("   • PACF: Decaimiento gradual\n")
    cat("   ► MODELO IDENTIFICADO: MA(", q_sugerido, ")\n\n")
    modelo_teorico <- paste0("MA(", q_sugerido, ")")
    p_final <- 0
    q_final <- q_sugerido
  } else if (patron_acf == "mixto" || patron_pacf == "mixto") {
    cat("   • ACF: Decaimiento gradual\n")
    cat("   • PACF: Decaimiento gradual\n")
    cat("   ► MODELO IDENTIFICADO: ARMA(", p_sugerido, ",", q_sugerido, ")\n\n")
    modelo_teorico <- paste0("ARMA(", p_sugerido, ",", q_sugerido, ")")
    p_final <- p_sugerido
    q_final <- q_sugerido
  } else {
    cat("   • Patrón no concluyente\n")
    cat("   ► Se sugiere probar varios modelos\n\n")
    p_final <- min(p_sugerido, 2)
    q_final <- min(q_sugerido, 2)
    modelo_teorico <- paste0("ARMA(", p_final, ",", q_final, ")")
  }

  # ============================================================
  # 4. MODELO ARIMA COMPLETO
  # ============================================================
  cat("═══ 4. MODELO ARIMA PROPUESTO ═══\n\n")

  modelo_arima <- paste0("ARIMA(", p_final, ",", d, ",", q_final, ")")

  cat("📦 MODELO FINAL:", modelo_arima, "\n\n")
  cat("Donde:\n")
  cat("   • p =", p_final, "→ Orden del componente autorregresivo (AR)\n")
  cat("   • d =", d, "→ Orden de diferenciación\n")
  cat("   • q =", q_final, "→ Orden del componente de media móvil (MA)\n\n")

  # ============================================================
  # 5. JUSTIFICACIÓN TEÓRICA
  # ============================================================
  cat("═══ 5. JUSTIFICACIÓN TEÓRICA ═══\n\n")

  cat("🎓 FUNDAMENTO:\n\n")

  if (d > 0) {
    cat("1. DIFERENCIACIÓN (d =", d, "):\n")
    cat("   • Test ADF inicial: p-valor =", round(adf_test$p.value, 4), "> 0.05\n")
    cat("   • La serie original no era estacionaria\n")
    cat("   • Tras", d, "diferenciación(es), se alcanza estacionariedad\n")
    cat("   • Justificación: Necesario para aplicar ARMA\n\n")
  } else {
    cat("1. DIFERENCIACIÓN (d = 0):\n")
    cat("   • Test ADF: p-valor =", round(adf_test$p.value, 4), "≤ 0.05\n")
    cat("   • La serie es estacionaria en media y varianza\n")
    cat("   • No se requiere diferenciación\n\n")
  }

  if (p_final > 0) {
    cat("2. COMPONENTE AR (p =", p_final, "):\n")
    cat("   • PACF muestra", length(pacf_sig), "rezagos significativos\n")
    if (patron_pacf == "corte_abrupto") {
      cat("   • Corte abrupto en PACF después del rezago", p_final, "\n")
      cat("   • Indica dependencia lineal con", p_final, "observaciones pasadas\n")
    } else {
      cat("   • Patrón de decaimiento sugiere componente autorregresivo\n")
    }
    cat("   • Justificación: X_t depende de {X_{t-1}, ..., X_{t-", p_final, "}}\n\n")
  }

  if (q_final > 0) {
    cat("3. COMPONENTE MA (q =", q_final, "):\n")
    cat("   • ACF muestra", length(acf_sig), "rezagos significativos\n")
    if (patron_acf == "corte_abrupto") {
      cat("   • Corte abrupto en ACF después del rezago", q_final, "\n")
      cat("   • Indica dependencia con", q_final, "errores pasados\n")
    } else {
      cat("   • Patrón de decaimiento sugiere componente de media móvil\n")
    }
    cat("   • Justificación: X_t depende de {ε_{t-1}, ..., ε_{t-", q_final, "}}\n\n")
  }

  # ============================================================
  # 6. VERIFICACIÓN CON AUTO.ARIMA
  # ============================================================
  cat("═══ 6. VERIFICACIÓN AUTOMÁTICA ═══\n\n")

  modelo_auto <- auto.arima(serie_original,
    seasonal = FALSE,
    stepwise = FALSE, approximation = FALSE
  )

  cat(
    "🤖 Modelo de auto.arima():",
    paste0(
      "ARIMA(", modelo_auto$arma[1], ",", modelo_auto$arma[6], ",",
      modelo_auto$arma[2], ")"
    ), "\n"
  )
  cat("📊 AIC =", round(modelo_auto$aic, 2), "\n")
  cat("📊 BIC =", round(modelo_auto$bic, 2), "\n\n")

  if (modelo_auto$arma[1] == p_final && modelo_auto$arma[6] == d &&
    modelo_auto$arma[2] == q_final) {
    cat("✅ COINCIDENCIA: El análisis teórico coincide con auto.arima()\n\n")
  } else {
    cat("⚠ DISCREPANCIA: Diferencias con auto.arima()\n")
    cat("   Posibles razones:\n")
    cat("   • Criterios de información (AIC/BIC) favorecen otro modelo\n")
    cat("   • Patrones en ACF/PACF no son completamente claros\n")
    cat("   • Se sugiere comparar ambos modelos\n\n")
  }

  # ============================================================
  # 7. RECOMENDACIONES
  # ============================================================
  cat("═══ 7. RECOMENDACIONES PRÁCTICAS ═══\n\n")

  cat("📌 PASOS SIGUIENTES:\n\n")
  cat("1. Ajustar el modelo propuesto:", modelo_arima, "\n")
  cat("   modelo <- Arima(serie, order = c(", p_final, ",", d, ",", q_final, "))\n\n")

  cat("2. Verificar significancia de coeficientes:\n")
  cat("   • Usar test t: |coef/se| > 1.96\n")
  cat("   • Eliminar coeficientes no significativos\n\n")

  cat("3. Validar supuestos sobre residuos:\n")
  cat("   • Normalidad: shapiro.test(residuals(modelo))\n")
  cat("   • Independencia: Box.test(residuals(modelo), type='Ljung-Box')\n")
  cat("   • Media cero: t.test(residuals(modelo))\n\n")

  cat("4. Comparar con modelos alternativos:\n")
  if (p_final > 0) cat("   • ARIMA(", p_final - 1, ",", d, ",", q_final, ")\n")
  if (q_final > 0) cat("   • ARIMA(", p_final, ",", d, ",", q_final - 1, ")\n")
  if (p_final > 0 && q_final > 0) {
    cat("   • ARIMA(", p_final + 1, ",", d, ",", q_final, ")\n")
    cat("   • ARIMA(", p_final, ",", d, ",", q_final + 1, ")\n")
  }
  cat("\n")

  cat("════════════════════════════════════════════════════════════════\n\n")

  # Retornar resultados
  invisible(list(
    modelo_propuesto = modelo_arima,
    p = p_final,
    d = d,
    q = q_final,
    modelo_auto = modelo_auto,
    adf_pvalue = adf_test$p.value,
    acf_significativos = acf_sig,
    pacf_significativos = pacf_sig,
    patron_acf = patron_acf,
    patron_pacf = patron_pacf
  ))
}
