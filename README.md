## SRTM Digital Elevation Model generation

This repository contains the application files and scripts to generates a digital elevation model (DEM) to be used with ROI_PAC, GMTSAR or GAMMA Synthetic Aperture Radar interferometry toolboxes.

## Quick link

* [Getting Started](#getting-started)
* [Installation](#installation)
* [Submitting the workflow](#submit)
* [Community and Documentation](#community)
* [Authors](#authors)
* [Questions, bugs, and suggestions](#questions)
* [License](#license)

### <a name="getting-started"></a>Getting Started

While the Geohazards Exploitation Platform hosts this service, you may use it in a sandbox to evolve it to e.g. support additional formats.

To run this application you will need a Developer Cloud Sandbox, that can be either requested from:
* ESA [Geohazards Exploitation Platform](https://geohazards-tep.eo.esa.int) for GEP early adopters;
* ESA [Research & Service Support Portal](http://eogrid.esrin.esa.int/cloudtoolbox/) for ESA G-POD related projects and ESA registered user accounts
* From [Terradue's Portal](http://www.terradue.com/partners), provided user registration approval.

A Developer Cloud Sandbox provides Earth Sciences data access services, and helper tools for a user to implement, test and validate a scalable data processing application. It offers a dedicated virtual machine and a Cloud Computing environment.
The virtual machine runs in two different lifecycle modes: Sandbox mode and Cluster mode.
Used in Sandbox mode (single virtual machine), it supports cluster simulation and user assistance functions in building the distributed application.
Used in Cluster mode (a set of master and slave nodes), it supports the deployment and execution of the application with the power of distributed computing for data processing over large datasets (leveraging the Hadoop Streaming MapReduce technology).

### <a name="installation"></a>Installation

#### Pre-requisites

This application requires mounting a volume with the SRTM tiles. This can be requested for via the Platform support.

##### Using the releases

Log on the developer cloud sandbox. Download the rpm package from https://github.com/Terradue/srtm-dem/releases.
Install the downloaded package by running these commands in a shell:

```bash
sudo yum -y install srtm-dem-<version>-ciop.x86_64.rpm
```

#### Using the development version

Log on the developer sandbox and run these commands in a shell:

```bash
cd
git clone git@github.com:Terradue/srtm-dem.git
git checkout develop
cd srtm-dem
mvn install
```

### <a name="submit"></a>Submitting the workflow

Run this command in a shell:

```bash
ciop-run
```
Or invoke the Web Processing Service via the Sandbox dashboard or the [Geohazards Thematic Exploitation platform](https://geohazards-tep.eo.esa.int) providing a product by reference to its catalogue entry, e.g.:

http://catalogue.terradue.int/catalogue/search/ASA_IM__0P/ASA_IM__0CNPDE20090412_092426_000000162078_00079_37207_1556.N1/rdf (master)


To learn more and find information go to

* [Developer Cloud Sandbox](http://docs.terradue.com/developer) service
* [ESA Geohazards Exploitation Platform](https://geohazards-tep.eo.esa.int)

### <a name="authors"></a>Authors (alphabetically)

* Barchetta Francesco
* Brito Fabrice
* D'Andria Fabio

### <a name="questions"></a>Questions, bugs, and suggestions

Please file any bugs or questions as [issues](https://github.com/Terradue/srtm-dem/issues/new) or send in a pull request.

### <a name="license"></a>License

Copyright 2015 Terradue Srl

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
