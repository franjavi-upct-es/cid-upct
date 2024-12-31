library(ggplot2)
library(tibble)

set.seed(314159)
h <- 0.5
bw <- 2 * h / sqrt(12)
values <- tibble(x = rnorm(100, 5, 1), y = 0)

colors <- c(
    "rectangular" = "red",
    "gaussiano" = "blue",
    "epanechnikov" = "green")
plot <- values %>%
    ggplot(aes(x = x)) +
    geom_point(aes(y = y)) +
    geom_density(aes(color = "rectangular"), alpha = 0.5, kernel = "rectangular", bw = bw) +
    geom_density(aes(color = "gaussiano"), alpha = 0.5, kernel = "gaussian", bw = bw) +
    geom_density(aes(color = "epanechnikov"), alpha = 0.5, kernel = "epanechnikov", bw = bw) +
    labs(
        title = "100 valores observados, estimación núcleo",
        y = "Densidad"
    ) +
    scale_color_manual(
        name = "Núcleo",
        breaks = c("rectangular", "gaussiano", "epanechnikov"),
        values = colors
)
ggsave("Figure 6.png", plot = plot, width = 15, height = 6, dpi = 1200)