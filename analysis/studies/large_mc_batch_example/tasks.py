from datetime import datetime
import b2luigi as luigi 

from analysis.studies.calculate_whizard_cross_section_example import DownloadWhizardSinFile
from src.mc_production.tasks import _create_mc_stage_classes, MCProductionWrapper
from src.mc_production.production_types import get_mc_production_types
from src import dataprod_config 

mc_stage_tasks = _create_mc_stage_classes(inject_stage1_dependency=DownloadWhizardSinFile)
class MCProductionWrapper(MCProductionWrapper):    
    def requires(self):
        for datatype in dataprod_config["datatype"]:
            yield mc_stage_tasks['stage2'](
                prodtype=get_mc_production_types()[self.prodtype], datatype=datatype
            )

if __name__ == "__main__":
    start = datetime.now()
    luigi.set_setting('batch_system', 'slurm')
    luigi.process(
        MCProductionWrapper(
        prodtype = dataprod_config['prodtype']
        ),
    batch=True,
    workers=20
    )
    stop = datetime.now()-start
    print(f'Run time was {stop}')

    
