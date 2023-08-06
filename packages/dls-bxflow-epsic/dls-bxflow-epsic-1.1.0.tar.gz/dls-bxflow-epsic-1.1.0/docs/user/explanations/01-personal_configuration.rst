
Personal Configuration
=======================================================================

A personal configuration runs a local, personal instasnce of the bxflow services.

It is intended for familiarization and workflow development.

In contrast to a personal configuration, a visit configuration is used during a beamline visit.

The following table illustrates some of the differences between a personal and a visit configuration.

.. list-table:: 
   :header-rows: 1

   * - 
     - workflow definitions
     - registry location
     - data_label
     - output location
     - HPC   
     - ispby 
     - auto trigger
   * - personal     
     - current working directory
     - /dls/tmp/$USER/${repository_name}/databases
     - full path
     - /dls/tmp/$USER/${repository_name}/outputs   
     - yes   
     - no
     - no
   * - visit     
     - <visit>/processing/dls-bxflow-epsic-workflows/workflows
     - <visit>/processing/dls-bxflow-epsic-workflows/database
     - scan number
     - <visit>/procssing/<scan>.bxflows
     - yes   
     - yes
     - yes

