# FLARE Examples 
Here we will discuss how to setup and run the examples stored in this repo.
<details><summary>Prerequisites</summary>
Flare is a python package and as such requires a python installation to be useable on your machine. 

Flare also does not provide the commandline tools upon which the workflow management tools operate. These commandline tools include

- FCCAnalysis
- Madgraph 5
- Pythia8
- Whizard

All of these commandline tools are available from the [Key4HEP stack](https://github.com/key4hep) which is provided by the CVMFs. 
</details>

<details><summary> Installation</summary>
To begin, install hep-flare using your package manager
```
pip install hep-flare
```
Next, familiarise yourself with the flare CLI tool 

```
flare --help
```

```
flare run --help 
```

Finally, run some code! 

## NOTE
As stated in [Prerequisites](#prerequisites) the underlying packages which Flare automates is not provided by Flare itself. All packages are available via the Key4HEP stack. If using a CVMFs powered machine you can run the following to setup Key4HEP

```
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```
</details>

<details><summary> Setup </summary>
Inside each example directory there is a `flare.yaml` which is the configuration file which flare will use to access and manage any settings the user wishes to change. You may wish to change the batch system to one of the available for b2luigi depending on your required batch system ([b2luigi batch systems](https://b2luigi.belle2.org/features/batch.html#batch-system-specific-settings)). To do this we update the `batch_system` variable inside the `flare.yaml` file like so 

``` 
# flare.yaml
batch_system : htcondor
```
A batch system is not strictly required and if none is passed to the `flare.yaml` then the `local` option is set. This means the Flare workflow will be ran entirely on your current head process. This is almost always slower but helpful for testing as it will fail fast and the stderr is printed to the terminal, rather than kept inside the `logs` directory. 

Other than this, we can override these settings from the Flare run commandline tool. There is a settings hierarchy used in Flare that follows this order 

## First Class Settings
If a setting is set directly from the commandline this is the setting that will be used. If the same setting is set via lower class, this is ignored for the first class setting that was passed

## Second Class Settings
If a setting is not set via the commandline tool but is instead set inside the `flare.yaml` then these settings are used during runtime

## Third Class Settings (Defaults)
Each Flare commandline setting has a default and if no [First Class](#fist-class-settings) or [Second Class](#second-class-settings) are defined then the defaults are used. These are:

``` python
class UserConfigModel(BaseModel):
    name: str = Field(default="default_name")
    version: str = Field(default="1.0")
    description: str = Field(default="No Description")
    studydir: Path | str = Field(default_factory=Path.cwd)
    outputdir: Path | str = Field(default_factory=Path.cwd)
```
</details>
<details><summary> FCCAnalysis Workflow Examples </summary>
Here we will discuss the examples located inside the [FCCAnalysis_workflow](https://github.com/CamCoop1/FLARE-examples/tree/main/FCCAnalysis_workflow) directory.

## Higgs Mass
We must first acknowledge that the scripts for this example are taken directly from Steering script taken from the [FCCAnalysis FCCee mH-recoil example](https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/FCCee/higgs/mH-recoil). The exact version of FCCAnalysis required to run this example is shown below

```
source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2025-05-29
```

To begin, `cd` into `FccAnalysis_workflow/higgs_mass_example`, in here you will find all the files setup ready to be used. Notably, all each python script for each stage of our FCCAnalysis workflow is prefixed by their unique stage identifier. 

```
stage1 -> stage1_flavor.py
stage2 -> stage2_histmaker_flavor.py
plots -> plots_flavor.py
```

With this in mind we can now run our workflow. To do this, we invoke the `flare` commandline tool and select the `run analysis` subcommand as shown below
```
flare run analysis 
```

## Add Stage Example
The Add Stage feature came with version flare 0.3.0. It allows a user to package and insert their own Flare Tasks into their workflow. We do this by adding to the `flare.yaml` an `add_stage` argument. 

``` YAML 
add_stage:
       HelloWorld:
        cmd: python3 {0}
        args:
          - ml_<>.py
        output_file: output.model
        requires: 'Stage2'

       Combine:
        cmd: python3 {0}
        args:
           - combine_<>.py
        output_file: output.model
        requires: 'helloworld'

       Move:
        cmd: python3 {0}
        args:
           - move_<>.py
        output_file: output.model
        requires: 'stage2'
        required_by : ['plots']
```

Each sub-argument of `add_stage` is a bundle that encapsulates everything Flare needs to know to create a Task. The `cmd` is the command that you wish to wrap with numbered curly braces for formatting. The `args` is the list of ordered arguments to go into our ordered `cmd` formatted curly braces. `output_file` is the output directory name. Then lastly, each bundle must have at least one `requires` (string) or `required_by` (list of string) arguments. This is how we tell Flare the order in which to insert our custom Tasks. 

To run this example, we invoke the `flare` commandline too like so:

``` 
flare run analysis
```


</details>
<details><summary> MCProduction Workflow Examples </summary>
Here we will discus the MC production capabilities of Flare. This workflow manager aims to provide the tools to make multi-detector analysis easy at the FCC. We will discuss how we can generate MC for different:

- Detector configurations
- MC generators
- Local versions of MC generators (instead of usings ones provided by Key4HEP) 



# Large Batch Example - Single MC Generator
This example we intend to show how one can generate a large quantity of MC types automatically using Flare. To begin, `cd` into the `MCProduction_workflow/large_mc_batch_example`. Note there is a `flare.yaml` and an `mc_production` directory inside. We seperate the MC production files into their own folder to keep things tidy. Inside the this `mc_production` directory is a `flare_mc.yaml` this is how we configure our MC production workflow. 

``` YAML
# flare_mc.yaml
global_prodtype : whizard

datatype:
    - wzp6_ee_nunuH_Hbb_ecm240
    - wzp6_ee_mumuH_Hbb_ecm240
    - wzp6_ee_bbH_HWW_ecm240
    - wzp6_ee_bbH_Hbb_ecm240
```
This is what it looks like, we declare the `global_prodtype` this is the MC generator we want to use for **ALL** the MC we generate. Then `datatype` which is a list of unique names, you'll note these names match the `.sin` files in our `mc_directory`. This is how Flare will find these files. 

To run this example, invoke the flare CLI tool like so:


```
flare run mcproduction
```

# Large Batch Multi Production Type Example - Multiple MC Generators 
This example shows how Flare can generate different MC using different generators all in a single workflow. Below is the `flare_mc.yaml` that makes this happen. Note that now we do not declare a `global_prodtype` rather we create a dictionary under each `datatype` entry which declares its own `prodtype` allowing us to declare on a MC type basis what generator we wish to use. 

``` YAML
# flare_mc.yaml
datatype:
    - wzp6_ee_mumuH_Hbb_ecm240:
        prodtype: whizard
    - wzp6_ee_bbH_HWW_ecm240:
        prodtype: whizard
    - wzp6_ee_bbH_Hbb_ecm240:
        prodtype: whizard
    - p8_ee_WW_ecm240: 
        prodtype : pythia8
    - p8_ee_ZZ_ecm240: 
        prodtype : pythia8
    - p8_ee_ZH_ecm240 : 
        prodtype : pythia8
```

To run this example, invoke the Flare CLI tool again:

```
flare run mcproduction
```

# Multiple Detector - Single MC Generator
In this example, we show how Flare can generator MC using different detector configuations. Below is the `flare_mc.yaml` which makes this happen. Note we are setting our `global_prodtype` to be Whizard and again have declared our list of `datatype`. However now we are declaring the `card`, which is a list of the different detector configuration cards that we wish to use inside our `mc_production` directory. Flare will then take each unique combination of `datatype` and `card` and create a Task. This results in 24 unique Tasks which Flare will orchestrate. 

``` YAML
# flare_mc.yaml

global_prodtype : whizard

datatype:
    - wzp6_ee_nunuH_Hbb_ecm240
    - wzp6_ee_mumuH_Hbb_ecm240
    - wzp6_ee_bbH_HWW_ecm240
    - wzp6_ee_bbH_Hbb_ecm240
    
card:
    - card_IDEA
    - card_IDEA_SiTracking
    - card_IDEA_3T
    - card_IDEA_lighterVXD_35pc
    - card_IDEA_lighterVXD_50pc
    - card_IDEA_better_singlehitReso_30pc_lighterVXD_50pc
```

Again, to run this example invoke the Flare CLI:

```
flare run mcproduction
```

# Multiple Detector - Multiple MC Generators 
Much like in the [Large Batch Multi Production Type Example - Multiple MC Generators](#large-batch-multi-production-type-example---multiple-m-generators) we can also generate MC for multiple different detector configurations whilst using different MC generators. The `flare_mc.yaml` which makes this happen is shown below.

``` YAML
# flare_mc.yaml
datatype:
    - wzp6_ee_mumuH_Hbb_ecm240:
        prodtype: whizard
    - p8_ee_WW_ecm240: 
        prodtype : pythia8
    - p8_ee_ZZ_ecm240: 
        prodtype : pythia8
    - p8_ee_ZH_ecm240 : 
        prodtype : pythia8
card:
    - card_IDEA
    - card_IDEA_lighterVXD_35pc
    - card_IDEA_lighterVXD_50pc
    
``` 

Again, to run this example invoke the Flare CLI:

```
flare run mcproduction
```

</details>

<details><summary> MC Production and FCCAnalysis Workflows </summary>
    The FCCAnalysis and MC production workflows are also able to be connected to form an even larger workflow. This is shown in the example below 

# Fastsim Multi Detector
In this example, we will be conducting a Multi Detector study at the FCCee. To do this we have our FCCAnalysis scripts inside `FCCAnalysis_and_MCProduction_workflow/example_fastsim_multidetector_mc` along with our MC Production scripts inside `FCCAnalysis_and_MCProduction_workflow/example_fastsim_multidetector_mc/mc_production`. With all of this in place, we can run this example using the below Flare CLI command, ensuring we are cd'd into the example directory.

```
flare run analysis --mcprod
```
The `--mcprod` flag tells Flare that we wish to attach the MC Production workflow before our FCCAnalysis workflow and to pipe the outputs of the MC Production.


</details>


<details><summary>Custom_workflows</summary>
    Inside of the Flare framework we are able to create our own b2luigi workflows USING the already established Flare tasks. 

# Whizard Cross Section 
The whizard cross section calculation is a custom workflow that uses the flare functionality to take the whizard production step of the MC Production workflow and create our own workflow. To do this, we use the `get_args` cli tool
inside of `flare.cli.arguments`. By passing the parsed arguments to the `flare.process` function, flare handles the entire workflow for you. Run the following command to try it out

```
cd Custom_workflows/calculate_whizard_cross_section_example/
python3 calculate_whizard_cross_section.py --mcprod
```
</details>
