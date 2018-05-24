---
layout: post
date: 2016-03-18 06:15:21
title: Hola Mundo
author: oschvr
mail: os@oschvr.com
excerpt: Construyendo una extensión de Chrome y Firefox para combatir las noticias falsas.
tags: development, mexico, fake news, fakenews, verificado, chrome, firefox
lang: es_MX
image: https://s3-us-west-2.amazonaws.com/oscarchavez/posts/hola-mundo/images/large/mexico.jpg
---

# <= WORK IN PROGRESS =>

## ULTRAVERIFICADO
> #### Una extensión de **Chrome** y **Firefox** que te alerta sobre antecedentes falsos y sitios de noticias poco confiables.

Autor: [oschvr](https://twitter.com/oschvr)

_Última Actualización: **22/Mayo/2018**_

--
### <u>RECTIFICACIÓN DE USO</u>

> UTILIZAMOS **SETS DE DATOS ESTÁTICOS** PARA ENTRENAR UN MODELO PROBABILÍSTICO EN LA DETECCIÓN DE NOTICIAS. EN LA PRÁCTICA REAL, LA EFICACIA  DE ESTE MODELO PUEDE DEGRADARSE A MEDIDA QUE SALEN NUEVOS ARTÍCULOS. 
> 
> ##### ESTA ES UNA HERRAMIENTA BASADA EN PROBABILIDAD POR LO QUE NO SIEMPRE VA A FUNCIONAR CORRECTAMENTE. 
> ### USA TU CRITERIO.

--

### Hipótesis (Abstract)

A unos meses de las [**Elecciones Presidenciales del 2018 en Mexico**](https://es.wikipedia.org/wiki/Elecciones_federales_en_M%C3%A9xico_de_2018) (la carrera política más importante de nuestro país), México enfrenta una crisis increiblemente compleja, las noticias falsas, la desinformación, posverdad y los rumores sin fundamento son considerados por algunos como una arma de influencia.

En este artículo de investigación, exploramos publicaciones y herramientas como *Procesamiento de Lenguaje Natural*, *Análisis Emocional* y *Aprendizaje Automático*, para **DETECTAR LA POSTURA DE UNA AFIRMACIÓN**, es decir, si el **TITULO DE LA NOTA** esta: 

1. **(1) DE ACUERDO**
2. **(2) EN DESACUERDO**
3. **(3) DISCUTIENDO**
4. **(4) Ó NO TIENE RELACIÓN**

con la **NOTA** en cuestión. En [VR3](https://vr3.io) creemos que automatizar el proceso de detección de postura (*discutiblemente*) puede ayudar a agilizar el proceso de verificación de noticias falsas y representa un primer paso en la crisis de información.


## Introducción


Derivado del catastrófico resultado de las [Elecciones Presidenciales del 2016 en Estados Unidos](https://es.wikipedia.org/wiki/Elecciones_presidenciales_de_Estados_Unidos_de_2016), las recientes declaraciones sobre el mal uso de datos personales de millones de usuarios por parte de [Cambridge Analytica](http://www.eluniversal.com.mx/techbit/cambridge-analytica-mas-usuarios-de-facebook-fueron-afectados) en favor de influir el voto, la [creciente preocupación de los mexicanos](https://www.huffingtonpost.com.mx/2018/03/02/los-mexicanos-estan-muy-preocupados-por-las-fake-news-pero-no-saben-identificarlas_a_23375461/?utm_hp_ref=mx-noticias-falsas) por las noticias falsas y la [falta de solución legislativa](https://www.contramuro.com/noticias-falsas-sin-solucion-legislativa-actualmente/), hemos planteado recurrir a la ciencia de datos para intentar prevenir la influencia y mal uso de la información en Redes Sociales como **Facebook** y **Twitter**

Afortunadamente, un excelente grupo de [periodistas, comunicadores, y ciudadanos](http://www.latimes.com/espanol/mexico/la-es-mientras-mexico-enfrenta-su-propia-crisis-de-noticias-falsas-estos-periodistas-luchan-por-la-verdad-20180415-story.html) se organizó para crear [**verificado.mx**](https://verificado.mx). Este experimento se basa en gran parte en el esfuerzo continuo de estos ciudadanos y pretende complementar esta plataforma ciudadana.

Utilizando datasets obtenidos mayormete de las contribuciones de [verificado.mx](https://verificado.mx)
 un modelo que **detecte y etiquete** noticias falsas y sitios de noticias poco confiables. Alertaremos a los lectores y navegadores de las Redes Sociales **Facebook** y **Twitter**.
 
### FUENTES
 
 @article{riedel2017fnc,
    author = {Benjamin~Riedel and Isabelle~Augenstein and Georgios~P.~Spithourakis and Sebastian~Riedel},
    title = {A simple but tough-to-beat baseline for the {Fake News Challenge} stance detection task},
    journal = {CoRR},
    volume = {abs/1707.03264},
    year = {2017},
    url = {http://arxiv.org/abs/1707.03264}
}

