For this example we use Whizard to generate 3 different MC types

- ee_qqH_HWW
- ee_bbH_HBB
- ee_mumuH_Hbb

All at 240 CME. As of this example only the CLD detector and reconstruction is available in flare and so that is what we will use.

To make this happen inside out mc_production folder we need the following files


# Step 1: Whizard
We need our .sin files for each datatype

# Step 2: ddsim
Flare will be looking for two things

1. a .xml file which contains the detector configuration. Note for the CLD detector use a symlink to the one available in the CVMFS

   ln -s $K4GEO/FCCee/CLD/compact/CLD_o2_v07.xml mc_production/CLD_o2_v07.xml

2. a ddsim steering file with a prefix "ddsim" and suffix ".py. What goes inbetween these is your choice, in this example we made it "ddsim_cld_steer.py"

# Step 3: k4run

Flare will look for a k4run steering script with the prefix "k4run" and suffix ".py". In our example we made it "k4run_CLDReconstruction.py".

This can be a symlink to the centrally available CLD configuration in CVMFS

     ln -s $CLDCONFIG/share/CLDConfig/CLDReconstruction.py k4run_CLDReconstruction.py

Additionally, inside the flare\_mc.yaml file there is a variable which can be set called "k4run_sandbox". We added this as some steering scripts (e.g CLD detector and recon) have a large amount of accompaning python modules that are not able to be loaded unless in the same working directory as the steering script. What a user can do is pass the path to the directory in which all these additional files live. Flare will attach them via symlinking to the working directory of the k4run step and ensure all additional files are present


# Step 4: the flare_mc.yaml
Inside here we set the following 

       ``` yaml
       '$model' : UserMCProdConfigModel

       global_prodtype : whizard_fullsim

       datatype:
       	- wzp6_ee_mumuH_Hbb_ecm240
	- wzp6_ee_bbH_Hbb_ecm240
       	- wzp6_ee_qqH_HWW_ecm240       
       ```

# Running Flare
To run flare, we simply invoke the flare CLI

   flare run mcproduction

And it will run.

# Current configuration
Currently it is configured (inside flare.yaml) to submit to the Slurm batch system. 