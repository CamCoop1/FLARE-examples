# FLARE Examples 
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

# Setup 
Inside the `analysis/config/details.yaml` is the main settings for the FLARE workflow. You may wish to change the batch system to one of the available for b2luigi depending on your required batch system ([b2luigi batch systems](https://b2luigi.belle2.org/usage/batch.html?highlight=batch#batch-system-specific-settings))
Other than this, we can override these settings from the flare commandline tool

# Higgs Mass
To run the higgs mass example, the easiest way is to submit the following command

```
flare run analysis --version higgs_mass --study-dir analysis/studies/higgs_mass_example  --config-yaml analysis/config/ 
```
# Large Batch Example
To run the Large Batch Example, the easiest way is to submit the following command

```
flare run mcproduction --version=large_mc_batch_example --study-dir analysis/studies/large_mc_batch_example  --config-yaml analysis/config/ 
```

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

