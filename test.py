from modules import histogram, earth_images 

# Calcular la firma espectral
firma_espectral = earth_images.get_spectral_signature(
    longitud=-70.4967607, 
    latitud=-12.0545491,    
    fecha_inicio='2024-01-01', 
    fecha_fin='2024-12-31'
)

# Graficar el histograma
histogram.plot_spectral_histogram(firma_espectral, lugar="Región")