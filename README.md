# Web Scraping sobre el sitio vvb.com.mx

Código para hacer web scraping sobre el sitio vvb.com.mx utilizando Scrapy. Se extrajeron 381 productos con el objetivo de analizar la variedad de oferta de la empresa, en un periodo aproximado de 2 minutos y 55 segundos.

Cada elemento extraído consta de:
* Producto.
* Bodega.
* País.
* Mundo.
* Tipo.
* URL.

El código fue depurado y optimizado para solucionar los problemas existentes debido a la estructura de los datos, dado que estos varían en algunos productos, lo que provocó que durante las primeras ejecuciones del script no se obtuvieran todos los elementos.

Se anexa un archivo log que muestra el proceso de extracción de datos, llamado vvb_output.txt.