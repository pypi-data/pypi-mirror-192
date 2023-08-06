import pathlib
import shutil
import subprocess
import tempfile
from warnings import warn

from gradescope_auto_py.grader_config import GraderConfig

folder_src = pathlib.Path(__file__).parent


def build_autograder(file_template, file_zip_out=None, include_folder=False,
                     verbose=True, **kwargs):
    """ builds a directory containing autograder in gradescope format

    Args:
        file_template (str): template file, used to generate a list of asserts
            for points
        file_zip_out (str): name of zip to create (contains setup.sh,
            requirements.txt, run_autograder.py & config.txt).  defaults to
            same name as assignment with zip suffix
        include_folder (bool): if True, all files in folder of file_template
            are included in autograder zip.  they'll be unpacked next to
            student submitted files (overwriting student files if name
            conflicts)
        verbose (bool): toggles message to warn user to set "autograder points"

    Returns:
        file_zip_out (pathlib.Path): zip file created
    """
    # make temp directory (contents will be zipped)
    folder_tmp = pathlib.Path(tempfile.mkdtemp())

    # move file_assign, run_autograder.py & setup.sh to folder
    file_template = pathlib.Path(file_template).resolve()
    for file in [folder_src / 'run_autograder',
                 folder_src / 'setup.sh',
                 file_template]:
        shutil.copy(file, folder_tmp / file.name)

    # build config.json in folder
    grader_config = GraderConfig.from_py(file_template=file_template, **kwargs)
    grader_config.to_json(folder_tmp / 'config.json')

    if include_folder:
        # copy all files
        folder_include = folder_tmp / 'include'
        shutil.copytree(file_template.parent, folder_include)

        # delete file_run, if present, which should come from student
        (folder_include / grader_config.file_run).unlink(missing_ok=True)

        # remove any zip files from include (prevents previous autograders from
        # being included)
        for file_zip in folder_include.rglob('*.zip'):
            warn(f'removing zip file from include: {file_zip}')
            file_zip.unlink()

    # build requirements.txt
    process = subprocess.run(['pipreqs', folder_tmp])
    assert process.returncode == 0, 'problem building requirements.txt'

    # include quick .txt file with total points
    pts_total = sum([afp.pts for afp in grader_config.afp_list])
    with open(folder_tmp / 'total_points.txt', 'w') as f:
        print(pts_total, file=f)

    # zip it up
    if file_zip_out is None:
        file_zip_out = file_template.with_suffix('.zip')
    shutil.make_archive(file_zip_out.with_suffix(''), 'zip', folder_tmp)

    # clean up
    shutil.rmtree(folder_tmp)

    if verbose:
        print(f'finished building: {file_zip_out}')
        print(f'total points: {pts_total}')

    return file_zip_out
