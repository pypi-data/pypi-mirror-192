conflicts module
================

Query armed conflict events worldwide and visualize them using spatial aggregations.
This service aggregates, clusters, and filters thousands of armed conflict events using the raw `UCDP Candidate Events Dataset <https://ucdp.uu.se/downloads/index.html#candidate>`__ as the ground truth.

Please cite:

- Hegre, Håvard, Mihai Croicu, Kristine Eck, and Stina Högbladh (July 2020)
  Introducing the UCDP Candidate Events Dataset. Research & Politics

We are using a web mercator projection using a grid size being optimized for geographic visualization. Each grid cell has a count attribute representing the number of armed conflict events of the corresponding grid cell.
This API aggregates locations where some armed conflict took place using geospatial intelligence operations. The geospatial results support the GeoJSON and Esri Features format out of the box.

.. figure:: https://geospatial-ai.de/wp-content/uploads/2023/02/geoconflicts-aggregate-745x1024.png

    Aggregated armed conflict events of 24th February 2022

For example:

>>> from georapid.client import GeoRapidClient
>>> from georapid.factory import EnvironmentClientFactory
>>> from georapid.conflicts import aggregate
>>> from georapid.formats import OutFormat
>>> host = "geoconflicts.p.rapidapi.com"
>>> client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
>>> features_dict = aggregate(client, format=OutFormat.ESRI)

.. automodule:: georapid.conflicts
    :members: