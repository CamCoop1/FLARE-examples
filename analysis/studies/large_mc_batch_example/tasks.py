from datetime import datetime
import b2luigi as luigi 
import subprocess

from flare.src.mc_production.tasks import MCProductionWrapper
from flare.src.utils.tasks import OutputMixin
from flare.src.mc_production.mc_production_types import get_mc_production_types
from flare.src.mc_production.tasks import get_mc_prod_stages_dict
import flare
from flare.cli.arguments import get_args



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
        



class MCProductionWrapper(MCProductionWrapper):    
    def requires(self):
        mc_stage_tasks = get_mc_prod_stages_dict(inject_stage1_dependency=DownloadWhizardSinFile)
        for datatype in luigi.get_setting('dataprod_config')["datatype"]:
            yield mc_stage_tasks['stage2'](
                prodtype=get_mc_production_types()[self.prodtype], datatype=datatype
            )

if __name__ == "__main__":
    start = datetime.now()
    args = get_args()
    luigi.set_setting('batch_system', 'slurm')
    flare.process(
        MCProductionWrapper(
        prodtype = 'whizard'
        ),
    batch=True,
    workers=20,
    flare_args = args
    )
    stop = datetime.now()-start
    print(f'Run time was {stop}')

    
