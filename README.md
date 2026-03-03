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

With this in mind we can now run our workflow. To do this, we envoke the `flare` commandline tool and select the `run analysis` subcommand as shown below
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

To run this example, we envoke the `flare` commandline too like so:

``` 
flare run analysis
```


</details>
<details><summary> Large Batch Example </summary>
To run the Large Batch Example, the easiest way is to submit the following command

```
flare run mcproduction --version=large_mc_batch_example --study-dir analysis/studies/large_mc_batch_example  --config-yaml analysis/config/ 
```
)
# Whizard Cross Section 
The whizard cross section calculation is a custom workflow that uses the flare functionality to take the whizard production step of the MC Production workflow and create our own workflow. To do this, we use the `get_args` cli tool
inside of `flare.cli.arguments`. By passing the parsed arguments to the `flare.process` function, flare handles the entire workflow for you. Run the following command to try it out

```
python3 analysis/studies/calculate_whizard_cross_section_example/calculate_whizard_cross_section.py --version=large_mc_batch_example --study-dir analysis/studies/calculate_whizard_cross_section_example  --config-yaml analysis/config/ --mcprod
```

# Whizard Multiple Detector Card Example
The multiple detector example displays flare's ability to produce MC using any number of detector cards. The MC config yaml can be found inside the `analysis/studies/multiple_detector_card_example/mc_production/details.yaml`. 
To enable flare's multi-card capability, the user must set the `card` list in their config like so:

``` YAML
card : 
    - card_IDEA
    - card_IDEA_3T
    - card_IDEA_SiTracking
```

These names must match those of the cards in your `mc_production` directory. To run this example use the following command:

```
flare run mcproduction --study-dir analysis/studies/multiple_detector_card_example --config-yaml analysis/studies/multiple_detector_card_example
```

# Note
Instead of adjusting the commandline arguments, you can instead just change the settings inside the `analysis/config/details.yaml` each time you wish to run an example. Then, when you call the flare CLI or your own custom workflow (see [Whizard Cross Section](#whizard_cross_section))
just parse the `--config-yaml` argument like so:

```
flare run analysis --config-yaml analysis/config
flare run mcproduction --config-yaml analysis/config
python3 custom_workflow.py --config-yaml analysis/config
```
</details>
