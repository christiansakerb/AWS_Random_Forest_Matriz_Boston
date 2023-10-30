# Project_MT_DS


## Problema que abordarán y su contexto

Una empresa anónima de Retail cuenta con un basto portafolio de productos, y presencia de estos en diferentes países, lo anterior la ubica como empresa líder en muebles y referencia para innovación y diseño de los mismos para todo tipo de necesidades en el hogar, lo anterior representa un reto en cuanto a administración, abastecimiento, rentabilidad y decisiones se trata.

Para lo anterior la empresa cuenta con un sistema de categorización de los distintos códigos que posee, el cual ha llamado matriz de contribución, dividiendo los productos entre 4 posibles cuadrantes, los cuales son: “Estrella”, “Imagen”, “Protectores”, e “interrogantes”

![Matriz de distribucion](https://raw.githubusercontent.com/christiansakerb/Project_MT_DS/main/imagen/matriz%20de%20distribucion.png)


Donde los productos Estrella son los productos que más contribución generan y más unidades mueven, mientras que los interrogantes son un grupo grande de productos que individualmente contribuyen muy poco y rotan muy poco. Por lo anterior cada cuadrante tiene su plan de acción en cuanto a su administración.
Esta categorización como se menciono antes tiene distintos fines en la optimización del portafolio, y se actualiza mensualmente, lo que significa que un producto que hoy es Estrella, puede no seguirlo siendo en el próximo mes, por lo que el plan que tenía cambiará al de su nuevo cuadrante. Sin embargo, al ser esta información utilizada para distintos fines la empresa desea anticiparse y detectar posibles caídas de los cuadrantes superiores a interrogantes para reducir sobreabastecimientos y sobrecostos.

### What data will you collect or create?
Este proyecto se basa en la utilización de datos reales de ventas en unidades y de la rentabilidad/contribución de muebles de una empresa cuyo nombre se mantiene confidencial, a la cual hemos tenido acceso desde el año 2021. Estos datos están almacenados en un datamart y se recopilan de manera continua. Los datos de ventas se obtienen diariamente a través del sistema de ventas y facturación de la empresa, y también del modelo de rentabilidad de productos. La información relacionada con los productos se encuentra en el repositorio de datos maestros, que incluye detalles como segmentos de productos, códigos, nombres, colores,
marcas, entre otros.
### How will the data be collected or created?
La información se recopila a partir de archivos en formato CSV proporcionados a los investigadores del proyecto. Estos archivos contienen información encriptada para preservar la confidencialidad de los datos.
Existen tres fuentes de información principales: Ventas_y_Rentabilidad: Un archivo CSV que contiene datos de ventas de productos desde el año 2021 hasta septiembre de 2023. Estos datos se presentan en un desglose mensual y están identificados por códigos de productos.
### How will you manage access and security?
Los datos residen en una instancia de AWS a la cual solo se puede acceder mediante las credenciales
proporcionadas por la Universidad y el par de claves utilizadas para la instancia en cuestión, que es la entidad
encargada de gestionar el acceso y la colaboración entre los miembros del proyecto. El acceso a la
información será abierto y sin restricciones para los cuatro investigadores principales, con el objetivo de no
obstaculizar el progreso de la investigación. Cabe destacar que los datos utilizados en los análisis son de
carácter privado.

### Integrantes 
Creator: Christian Saker
- Principal Investigator: Laura Rodriguez
- Data Manager: Brayan Torres, Jesica Vique
- Project Administrator: Christian Saker
Affiliation: Universidad de Los Andes (uniandes.edu.co)

