.. -*- coding: utf-8 -*-

.. _SPChartHelp:

============
SPChart Help
============

:Author: Aaron Lee 
:Revision: : $Revision$
:LastChangedDate: $LastChangedDate$ 

.. contents::
.. sectnum::


SPChart
=======

Overview
--------
SPChart is free software to plot S-paramters. The motivation of 
developing this software is that I cannot find a free tools
to do such things.

Features
--------
SPchart is still under developing and now it has features:

* support SnP files from S1P upto S9P
* only support 4 port mixed mode s-paramters
* export chart to eps, emf, pdf, png, ps, svg format
* phase functions
* TDR(not applied in this version)

License
-------
SPChart is free and open source software, it is free for any purpose.


Main Menus
==========

The File Menu
-------------
**Open** menu open SNP files, like "aaa.s4p" 

The Chart Menu
--------------
**(not applied)**

The Function Menu
-----------------
**TDR** (not applied)

**Phase** view phase paramters of current SNP files, it also support 
mixed mode s-paramters.

The Curve Menu
--------------
**All On** show all curves

**All Off** turn off all curves

**Reflections** Only show reflection curves, usually it is Sij 
where i=j, like S11, S22, S33, S44, etc. 

**Transmissions** Only show transmission curves,usually it is Sij
where i>j, like S21, S31, S41, S32, S42, S43, etc

**Isolations** Only show isolation curves,usually it is Sij
where i<j, like S12, S13, S14, S23, S24, S34, etc

**Custom Curve** Choose the curves you want by checkbox.

The Option Menu
---------------
**Chart Setting** Set chart options


The Help Menu
-------------
**Content** Help content

**About** show about me dialog.


Main Toolbars
=============


|CustomCurve| tool is custom curve dialog. 
You can choose the curve by name and display the curve you want.

.. |CustomCurve| image:: _static/CustomCurve.png 

|MixMode| tool is for mixed mode s-paramters

.. |MixMode| image:: _static/MixMode.png 

Chart interface
====================
This is a example of S4P file,

.. image:: _static/ChartInterface.png 

1. Menubar
2. Toolbar
3. Chart title display the file path
4. Y-Axis display name and unit
5. Chart legends is the legend for every curve
6. Chart Toolbar is toolbar for every chart
7. X-Axis display frequency and unit



Mixed Mode S-Paramters
======================
Mixed mode s-paramters dialog can be opened by Menu *Function-> Mixed Mod*
or by toolbar |MixMode|

In this version **only 4 ports s-paramters (s4p) is supported**

.. image:: _static/MixModeInterface1.png 

File Entry
----------
Browse the file to convert to mixed mode

Port Mapping
------------
It is important to set correct port mapping, usually the port map of 4 port system is like this,
and it is also the default setting of SPChart.

.. image:: _static/MixModPortMapping1.png

.. image:: _static/PortMappingGrid1.png




Sometimes the connection maybe swapped, and need change the port mapping manually, like this:

.. image:: _static/MixModPortMapping2.png

.. image:: _static/PortMappingGrid2.png

Chart Type
----------
It can display maglitude or angle.

Filter buttons
--------------
4 filter buttons can filter the S-Paramters quickly.





