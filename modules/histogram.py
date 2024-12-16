import matplotlib.pyplot as plt
import seaborn as sns

def plot_spectral_histogram(firma_espectral, lugar="Región"):
    """
    Genera un histograma de la firma espectral con nombres interpretables para bandas.
    Args:
        firma_espectral (dict): Valores promedio de reflectancia por banda.
        lugar (str): Nombre del lugar para el título del gráfico.
    """
    # Mapeo de bandas a términos descriptivos
    nombres_bandas = {
        'B1': '443 nm',  # Aerosoles Costeros
        'B2': '490 nm',  # Azul (Agua)
        'B3': '560 nm',  # Verde
        'B4': '665 nm',  # Rojo
        'B8': '842 nm',  # NIR
        'B11': '1610 nm',  # SWIR 1
        'B12': '2190 nm'  # SWIR 2
    }
    
    # Traducir las claves técnicas a nombres más descriptivos
    bandas_descriptivas = [nombres_bandas.get(banda, banda) for banda in firma_espectral.keys()]
    valores = list(firma_espectral.values())
    
    # Configuración de estilo moderno y colores vibrantes
    sns.set_theme(style="whitegrid")
    colores = sns.color_palette("viridis", len(bandas_descriptivas))
    
    # Crear el gráfico
    plt.figure(figsize=(14, 8))
    bars = plt.bar(
        bandas_descriptivas, 
        valores, 
        color=colores, 
        edgecolor='black', 
        linewidth=1.5
    )
    
    # Añadir etiquetas de valor encima de las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0, 
            height + 0.02, 
            f'{height:.2f}', 
            ha='center', 
            va='bottom', 
            fontsize=12, 
            color='black', 
            weight='bold'
        )

    # Personalizar el gráfico
    plt.title(f"Firma Espectral Promedio de {lugar}", fontsize=22, weight='bold', color="#4a4a4a")
    plt.xlabel("Cobertura Terrestre", fontsize=16, weight='bold', color="#4a4a4a")
    plt.ylabel("Reflectancia Promedio", fontsize=16, weight='bold', color="#4a4a4a")
    plt.xticks(fontsize=14, weight='bold', rotation=45)
    plt.yticks(fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Fondo claro para resaltar las barras
    plt.gca().set_facecolor('#f9f9f9')
    
    # Mejorar diseño general
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Ajustar diseño para evitar solapamientos
    plt.tight_layout()
    plt.show()
