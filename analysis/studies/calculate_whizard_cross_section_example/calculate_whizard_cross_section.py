import re
import subprocess
from pathlib import Path

import b2luigi as luigi
from astropy.units import fbarn as fb
from astropy.units import pbarn as pb

import flare
from flare.src.mc_production.mc_production_types import get_mc_production_types
from flare.src.mc_production.tasks import get_mc_prod_stages_dict
from flare.src.utils.tasks import OutputMixin
from flare.cli.arguments import get_args


# Branching fraction from 2024 PDG https://pdg.lbl.gov/2024/reviews/rpp2024-rev-higgs-boson.pdf
BFs = {
    "wzp6_ee_nunuH_Hbb_ecm240": 5.82e-1,
    "wzp6_ee_mumuH_Hbb_ecm240": 5.82e-1,
    "wzp6_ee_bbH_HWW_ecm240": 2.14e-1,
    "wzp6_ee_bbH_Hbb_ecm240": 5.82e-1,
}


class DownloadWhizardSinFile(OutputMixin, luigi.DispatchableTask):
    """
    Task for downloading the .sin files for a datatype
    """
    @property
    def results_subdir(self):
        return luigi.get_setting("results_subdir")
    
    datatype = luigi.Parameter()

    @property
    def output_dir(self):
        return luigi.get_setting("dataprod_dir")
    @property
    def raw_github_url(self):
        return f"https://raw.githubusercontent.com/HEP-FCC/FCC-config/refs/heads/winter2023/FCCee/Generator/Whizard/v3.0.3/{self.datatype}.sin"
    
    def output(self):
        output_file_name = f"{self.datatype}.sin"
        yield {output_file_name: luigi.LocalTarget(self.output_dir / output_file_name)}

    def process(self):
        cmd = ["wget", self.raw_github_url]
        _ = subprocess.check_output(cmd, cwd=self.output_dir)
        


class ExtractCrossSectionFromWhizardLog(OutputMixin, luigi.DispatchableTask):
    """
    Extract the cross section from the whizard.log file created during MCProductionStage1
    """

    prodtype = luigi.EnumParameter(enum=get_mc_production_types())
    datatype = luigi.Parameter()

    @property
    def results_subdir(self):
        return luigi.get_setting("results_subdir")

    @property
    def whizard_log_regrex(self):
        return r"(?m)^\s*15\s+\d+\s+([-+]?\d+\.\d+E[+-]\d+)"

    @property
    def output_file_name(self):
        return f"{self.datatype}_cs.txt"

    @property
    def stage1_whizard_log_file(self):
        task = next(self.requires())
        LocalTarget = next(iter(next(iter(task.output())).values()))
        parent_dir = Path(LocalTarget.path).parent

        whizard_log_generator = parent_dir.glob("whizard.log")
        return next(iter(whizard_log_generator))

    def requires(self):
        """
        Here we change the requires function on the Stage1 task for whizard
        to make it require the DownloadWhizardSinFile, which as the name suggest
        will download the .sin file from the public github
        """
        stage1_task = get_mc_prod_stages_dict(inject_stage1_dependency=DownloadWhizardSinFile)['stage1']
        yield self.clone(stage1_task)

    def output(self):
        yield self.add_to_output(self.output_file_name)

    @luigi.on_temporary_files
    def process(self):

        with self.stage1_whizard_log_file.open("r") as f:
            whizard_log = f.read()

        match = re.search(self.whizard_log_regrex, whizard_log)

        if match:
            cs_fb = float(match.group(1)) * fb
        else:
            raise ValueError(
                f"Cross section could not be found for {self.datatype} in the whizard log"
            )

        total_cs_fb = cs_fb * BFs[self.datatype]
        total_cs_pb = total_cs_fb.to(pb).value

        with open(self.get_output_file_name(self.output_file_name), "w") as f:
            f.write(f"{self.datatype}: {total_cs_pb}\n")


class CompileCrossSections(OutputMixin, luigi.DispatchableTask):
    """
    Get all the cross sections for each datatype and compile them into a single file
    """

    prodtype = luigi.EnumParameter(enum=get_mc_production_types())
    
    @property
    def results_subdir(self):
        return luigi.get_setting("results_subdir")

    def requires(self):
        for datatype in luigi.get_setting("dataprod_config")["datatype"]:
            yield ExtractCrossSectionFromWhizardLog(
                prodtype=self.prodtype, datatype=datatype
            )

    @property
    def output_file_name(self):
        return "compiled_cs.txt"

    def output(self):
        yield self.add_to_output(self.output_file_name)

    @luigi.on_temporary_files
    def process(self):
        for input_path in self.get_all_input_file_names():
            input_path = Path(input_path)

            with input_path.open("r") as f:
                total_cs_pd = f.read()

            with open(self.get_output_file_name(self.output_file_name), "a") as f:
                f.write(total_cs_pd)


if __name__ == "__main__":
    
    args = get_args()
    # build_executable_and_save_to_settings_manager(args)
    # load_settings_into_manager(args)
    flare.process(
        CompileCrossSections(
            prodtype=get_mc_production_types()["whizard"]
        ),
        batch=True,
        workers=10,
        ignore_additional_command_line_args=True,
        flare_args = args
    )
